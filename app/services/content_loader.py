"""Markdown content with YAML front-matter: content/<kind>/<slug>.md, or in a folder of its own,
content/<kind>/<folder>/<slug>.md, next to its drafts and notes. The folder name isn't part of the URL.
Files and folders starting with "_" or "." are skipped.

Required front-matter: title, description, published (YYYY-MM-DD).
Optional: updated, draft (true hides it), youtube_id (videos).
In the body, :logo-<slug>: shows the tool mark t-<slug> from partials/tool-logos.svg.
"""
import os
import re
from datetime import date
from functools import lru_cache
from html import unescape

import markdown
import yaml
from flask import current_app

REQUIRED = ("title", "description", "published")
LOGO = re.compile(r":logo-([a-z0-9]+):( [^\s<]+)?")
H2 = re.compile(r"<h2[^>]*>(.*?)</h2>", re.S)
TAG = re.compile(r"<[^>]+>")


def _logo(m):
    mark = f'<svg class="tool-mark" aria-hidden="true" focusable="false"><use href="#t-{m[1]}"/></svg>'
    # The mark stays on the same line as the word after it, so a wrapped cell never leaves it behind.
    return f'<span class="tool-name">{mark}{m[2].lstrip()}</span>' if m[2] else mark


def _parse(path):
    # utf-8-sig: Windows editors often save a byte-order mark, which would hide the opening "---".
    with open(path, encoding="utf-8-sig") as fh:
        raw = fh.read()
    if not raw.startswith("---"):
        raise ValueError(f"{path}: missing front-matter")
    _, fm, body = raw.split("---", 2)
    meta = yaml.safe_load(fm) or {}
    missing = [k for k in REQUIRED if k not in meta]
    if missing:
        raise ValueError(f"{path}: missing {', '.join(missing)}")
    for key in ("published", "updated"):
        if isinstance(meta.get(key), date):
            meta[key] = meta[key].isoformat()
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["path"] = path
    html = markdown.markdown(body, extensions=["extra", "sane_lists", "toc"])
    meta["logos"] = sorted({m[1] for m in LOGO.finditer(html)})
    meta["html"] = LOGO.sub(_logo, html)
    # For the featured card: the article's questions (its h2s) and a reading time at about 200 words a minute.
    meta["headings"] = [unescape(TAG.sub("", h)).strip() for h in H2.findall(html)]
    meta["minutes"] = max(1, round(len(unescape(TAG.sub(" ", html)).split()) / 200))
    return meta


def _files(folder):
    """The .md files in folder and in its subfolders, one level down."""
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if name.startswith(("_", ".")):
            continue
        if os.path.isdir(path):
            yield from (
                os.path.join(path, sub)
                for sub in sorted(os.listdir(path))
                if sub.endswith(".md") and not sub.startswith(("_", "."))
            )
        elif name.endswith(".md"):
            yield path


@lru_cache(maxsize=8)
def _load(content_dir, kind, _debug_bust):
    folder = os.path.join(content_dir, kind)
    if not os.path.isdir(folder):
        return ()
    items = [_parse(path) for path in _files(folder)]
    slugs = [i["slug"] for i in items]
    dupes = sorted({s for s in slugs if slugs.count(s) > 1})
    if dupes:
        raise ValueError(f"content/{kind}: more than one file named {', '.join(dupes)}.md")
    items = [i for i in items if not i.get("draft")]
    # Newest first. On the same date, the later file path first (article-2/ before article-1/).
    return tuple(sorted(items, key=lambda i: (i["published"], i["path"]), reverse=True))


def all_items(kind):
    cfg = current_app.config
    bust = os.urandom(4) if current_app.debug else None
    return list(_load(cfg["CONTENT_DIR"], kind, bust))


def get_item(kind, slug):
    return next((i for i in all_items(kind) if i["slug"] == slug), None)
