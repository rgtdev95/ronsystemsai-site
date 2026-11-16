# Content

Articles go in `resources/`, videos in `videos/`. One Markdown file per item; the file name becomes the URL slug.

An item can have a folder of its own, one level down, for its drafts and notes: `resources/article-2/how-ai-screens-job-listings-for-a-client.md` is published at `/resources/how-ai-screens-job-listings-for-a-client/`. The folder name isn't part of the URL, and two files with the same name in different folders stop the site with an error. On the same `published` date, the later folder or file is listed first.

```markdown
---
title: "n8n vs Zapier vs Make: which should a small business use?"
description: "A plain-English comparison of cost, limits and when to switch."
published: 2026-10-15
updated: 2026-10-15      # optional
draft: true              # optional; drafts are hidden
youtube_id: dQw4w9WgXcQ  # videos only
---

Start with a 40–60 word direct answer, then expand with question-shaped headings.
```

## Tool logos

Write `:logo-<slug>:` before a tool's name to show its mark, e.g. `| Automation | :logo-n8n: n8n | ... |`. The marks are the `t-<slug>` symbols in `app/templates/partials/tool-logos.svg` (one color, from Simple Icons). A test fails if an article uses a slug that isn't there. To add one, copy the icon's path from [Simple Icons](https://simpleicons.org) into a new `<symbol id="t-<slug>" viewBox="0 0 24 24">` in that file. Tools only, never client logos.

Files starting with `_` are ignored. See `docs/04-site-structure.md` for the article template and `docs/05-search-and-ai-visibility.md` for the writing rules.
