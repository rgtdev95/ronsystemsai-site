import json
import re
from html import unescape

import pytest

from app import create_app
from app import site_content as C


@pytest.fixture
def app():
    return create_app("testing")


@pytest.fixture
def client(app):
    return app.test_client()


PAGES = ["/", "/services/", "/process/", "/about/", "/faq/", "/book/", "/privacy/", "/terms/", "/resources/", "/videos/"]


@pytest.mark.parametrize("path", PAGES + [f"/services/{s['slug']}/" for s in C.SERVICES])
def test_pages_render(client, path):
    resp = client.get(path)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert html.count("<h1") == 1, "exactly one h1 per page"
    assert '<link rel="canonical"' in html
    assert "style=" not in html, "inline styles are blocked by the CSP"


def test_404(client):
    resp = client.get("/nope/")
    assert resp.status_code == 404
    assert "isn't on the rail" in resp.get_data(as_text=True)


def test_jsonld_is_valid_json(client):
    html = client.get("/").get_data(as_text=True)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert blocks
    types = {json.loads(b)["@type"] for b in blocks}
    assert {"ProfessionalService", "Person", "WebSite", "FAQPage"} <= types


def test_business_structured_data_has_logo(client):
    html = client.get("/").get_data(as_text=True)
    blocks = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
    org = next(b for b in blocks if b["@type"] == "ProfessionalService")
    logo_path = org["logo"]["url"].split("://", 1)[-1].split("/", 1)[1]
    assert client.get("/" + logo_path).status_code == 200, "logo file must be served"
    assert org["logo"]["width"] >= 112 and org["logo"]["height"] >= 112


def test_person_structured_data_has_a_served_photo(client):
    html = client.get("/about/").get_data(as_text=True)
    blocks = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
    person = next(b for b in blocks if b["@type"] == "Person")
    photo_path = person["image"].split("://", 1)[-1].split("/", 1)[1]
    assert client.get("/" + photo_path).status_code == 200


def test_no_prices_or_timezone_claims(client):
    for path in PAGES:
        text = client.get(path).get_data(as_text=True)
        assert not re.search(r"[$€£]\s?\d", text), f"price figure on {path}"
        assert "UTC" not in text and "time zone" not in text.replace("your own time zone", ""), f"time-zone claim on {path}"
        assert "Working with clients in" not in text


def test_robots_blocks_non_production(client):
    body = client.get("/robots.txt").get_data(as_text=True)
    assert "Disallow: /" in body


def test_robots_allows_ai_crawlers_in_production():
    client = create_app("production").test_client()
    body = client.get("/robots.txt").get_data(as_text=True)
    assert "GPTBot" in body and "ClaudeBot" in body and "Disallow" not in body
    assert "X-Robots-Tag" not in client.get("/").headers


def test_test_env_sends_noindex_header():
    client = create_app("test").test_client()
    assert client.get("/").headers["X-Robots-Tag"] == "noindex, nofollow"


def test_security_headers(client):
    csp = client.get("/").headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp and "frame-ancestors 'none'" in csp


def test_sitemap_lists_services(client):
    xml = client.get("/sitemap.xml").get_data(as_text=True)
    for s in C.SERVICES:
        assert f"/services/{s['slug']}/" in xml
    assert "/terms/" in xml


def test_sitemap_has_no_made_up_dates(app, client):
    # Pages built from code have no real "last modified" date, so the sitemap leaves it out.
    # Markdown items carry their own published/updated date; a listing takes its newest item's.
    from app.services import content_loader

    real = {}
    with app.app_context():
        for kind in ("resources", "videos"):
            dates = {f"/{kind}/{i['slug']}/": i.get("updated") or i["published"] for i in content_loader.all_items(kind)}
            if dates:
                real.update(dates)
                real[f"/{kind}/"] = max(dates.values())
    xml = client.get("/sitemap.xml").get_data(as_text=True)
    found = dict(re.findall(r"<loc>https?://[^/<]+(/[^<]*)</loc><lastmod>([^<]+)</lastmod>", xml))
    assert found == real


def test_missing_trailing_slash_redirects(client):
    # One URL per page: /about must not be a second copy of /about/.
    resp = client.get("/about")
    assert resp.status_code == 308
    assert resp.headers["Location"].endswith("/about/")


@pytest.mark.parametrize("path", PAGES + [f"/services/{s['slug']}/" for s in C.SERVICES])
def test_titles_and_descriptions_fit_search_results(client, path):
    html_text = client.get(path).get_data(as_text=True)
    title = unescape(re.search(r"<title>(.*?)</title>", html_text, re.S).group(1).strip())
    desc = unescape(re.search(r'<meta name="description" content="(.*?)">', html_text, re.S).group(1))
    assert len(title) <= 60, f"title {len(title)} chars: {title}"
    assert len(desc) <= 155, f"description {len(desc)} chars: {desc}"


def test_indexnow_key_file(app):
    client = app.test_client()
    assert client.get("/abc123.txt").status_code == 404, "no key configured"
    app.config["INDEXNOW_KEY"] = "abc123"
    resp = client.get("/abc123.txt")
    assert resp.status_code == 200 and resp.get_data(as_text=True) == "abc123"
    assert client.get("/other.txt").status_code == 404


@pytest.mark.parametrize("path", ["/favicon.ico", "/apple-touch-icon.png"])
def test_icons_are_served(client, path):
    assert client.get(path).status_code == 200


def test_empty_listings_are_noindex_in_production():
    from app.services import content_loader

    app = create_app("production")
    client = app.test_client()
    for kind in ("resources", "videos"):
        with app.app_context():
            empty = not content_loader.all_items(kind)
        robots = client.get(f"/{kind}/").headers.get("X-Robots-Tag")
        assert (robots == "noindex") == empty, kind


@pytest.mark.parametrize("env", ["production", "test"])
def test_no_page_sets_cookies(env):
    # The privacy page promises no cookies, so there's no cookie banner.
    client = create_app(env).test_client()
    for path in PAGES:
        assert "Set-Cookie" not in client.get(path).headers, f"cookie set on {path}"


def test_contact_redirects_to_book(client):
    resp = client.get("/contact/")
    assert resp.status_code == 301
    assert resp.headers["Location"].endswith("/book/")


def test_work_redirects_to_articles(client):
    resp = client.get("/work/")
    assert resp.status_code == 301
    assert resp.headers["Location"].endswith("/resources/")


def test_home_lists_the_latest_articles(app, client):
    from app.services import content_loader

    with app.app_context():
        latest = content_loader.all_items("resources")[:3]
    html = client.get("/").get_data(as_text=True)
    assert ("Latest articles" in html) == bool(latest)
    for item in latest:
        assert f'href="/resources/{item["slug"]}/"' in html
    assert 'href="/work/"' not in html


def test_newest_article_is_a_featured_card(app, client):
    from app.services import content_loader

    with app.app_context():
        latest = content_loader.all_items("resources")
    # The homepage shows each of its (up to) three articles as a card; /resources/ only the newest.
    for path, cards in (("/", min(3, len(latest))), ("/resources/", min(1, len(latest)))):
        html = client.get(path).get_data(as_text=True)
        assert html.count('class="job job--featured"') == cards, path
        for item in latest[:cards]:
            assert item["title"] in html and f'{item["minutes"]}-minute read' in html, path


def test_footer_shows_every_social_logo_but_links_only_set_urls(app):
    app.config["SOCIAL"] = {"YouTube": "", "Facebook": "", "LinkedIn": "https://example.com/in", "GitHub": ""}
    html = app.test_client().get("/").get_data(as_text=True)
    for name in ("youtube", "facebook", "linkedin", "github"):
        assert f'href="#i-{name}"' in html
    assert html.count('<a class="social__link"') == 1
    assert 'href="https://example.com/in"' in html
    assert html.count("social__link--off") == 3


def test_booking_button_only_when_url_is_set(app):
    client = app.test_client()
    app.config["BOOKING_URL"] = ""
    html = client.get("/book/").get_data(as_text=True)
    assert 'data-umami-event="booking-open"' not in html
    assert "Get in touch" in html

    app.config["BOOKING_URL"] = "https://calendar.proton.me/bookings#test"
    html = client.get("/book/").get_data(as_text=True)
    assert 'href="https://calendar.proton.me/bookings#test"' in html
    assert 'target="_blank" rel="noopener"' in html
    assert "Prefer to write?" in html


def test_book_offers_email_and_messaging_socials_only(app):
    app.config["SOCIAL"] = {"YouTube": "https://example.com/yt", "Facebook": "", "LinkedIn": "https://example.com/in", "GitHub": "https://example.com/gh"}
    html = app.test_client().get("/book/").get_data(as_text=True)
    assert f'href="mailto:{app.config["CONTACT_EMAIL"]}"' in html
    assert "Message me on LinkedIn" in html
    assert "Message me on Facebook" not in html, "empty URL, so no line"
    assert "Message me on YouTube" not in html and "Message me on GitHub" not in html
    assert "<form" not in html


def test_llms_txt(client):
    body = client.get("/llms.txt").get_data(as_text=True)
    assert body.startswith("# Ron Systems AI")


def test_healthz(client):
    assert client.get("/healthz").status_code == 200


def test_article_logos_are_in_the_sprite(app):
    from app.services import content_loader

    with app.app_context():
        sprite = app.jinja_env.loader.get_source(app.jinja_env, "partials/tool-logos.svg")[0]
        for kind in ("resources", "videos"):
            for item in content_loader.all_items(kind):
                for slug in item["logos"]:
                    assert f'id="t-{slug}"' in sprite, f"{item['slug']}: no mark t-{slug} in tool-logos.svg"


def test_content_with_byte_order_mark_loads():
    import pathlib
    import tempfile

    from app.services import content_loader

    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "bom.md"
        path.write_text("﻿---\ntitle: T\ndescription: D\npublished: 2026-01-01\n---\n:logo-n8n: n8n\n", encoding="utf-8")
        item = content_loader._parse(str(path))
    assert item["logos"] == ["n8n"] and 'href="#t-n8n"' in item["html"] and ":logo-" not in item["html"]


def _write_item(path, published="2026-01-01", draft=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    extra = "draft: true\n" if draft else ""
    path.write_text(f"---\ntitle: T\ndescription: D\npublished: {published}\n{extra}---\nBody\n", encoding="utf-8")


def test_content_can_sit_in_its_own_folder():
    import pathlib
    import tempfile

    from app.services import content_loader

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        _write_item(root / "resources" / "top.md")
        _write_item(root / "resources" / "article-1" / "older.md")
        _write_item(root / "resources" / "article-2" / "newer.md")
        _write_item(root / "resources" / "article-2" / "_rewrite.md")
        _write_item(root / "resources" / "_notes" / "skipped.md")
        _write_item(root / "resources" / "article-3" / "hidden.md", draft=True)
        slugs = [i["slug"] for i in content_loader._load(tmp, "resources", object())]
    # Same date: the later path comes first. The folder name isn't part of the slug.
    assert slugs == ["top", "newer", "older"]


def test_two_files_with_the_same_name_are_refused():
    import pathlib
    import tempfile

    from app.services import content_loader

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        _write_item(root / "resources" / "same.md")
        _write_item(root / "resources" / "article-1" / "same.md", draft=True)
        with pytest.raises(ValueError, match="same.md"):
            content_loader._load(tmp, "resources", object())
