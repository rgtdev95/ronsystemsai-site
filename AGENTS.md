# AGENTS.md

Instructions for AI coding agents working in this repo. Humans: start with [README.md](README.md).

## What this is

The marketing site for **Ron Systems AI** (ronsystemsai.com), the IT systems, automation and AI consultancy of Rolando "Ron" Tactay. Audience: non-technical owners and managers of small and medium businesses. The one goal is a booked discovery call.

- Product, audience and tone: [PRODUCT.md](PRODUCT.md)
- Visual design system (colors, type, components): [DESIGN.md](DESIGN.md)
- Decisions already made, with reasons: [docs/08-open-decisions.md](docs/08-open-decisions.md). Don't re-open them without asking.
- What's still open: [docs/07-launch-checklist.md](docs/07-launch-checklist.md), section "Next session"

## Stack

Flask 3 + Jinja2, server-rendered. Plain CSS and JavaScript, no framework and no build step. Markdown files for articles and videos. Python 3.12. Gunicorn in Docker on a VPS behind Caddy. Umami analytics.

## Commands

```bash
uv venv --python 3.12                     # once
uv pip install -r requirements.txt        # one dependency file for everything
uv run flask --app wsgi run --debug       # http://127.0.0.1:5000; loads .env automatically
uv run pytest -q                          # must pass before you finish
uv run ruff check app tests wsgi.py       # must pass before you finish
docker build -f docker/Dockerfile .       # from the project root
```

## Where things live

| What | Where |
|---|---|
| Page copy (hero, services, process, FAQs, case studies, tools) | `app/site_content.py` |
| Routes | `app/routes/pages.py`, `content.py` (articles/videos), `seo.py` (robots, sitemap, llms.txt, icons, IndexNow key) |
| Structured data (JSON-LD) | `app/services/schema.py` |
| Templates | `app/templates/` (`base.html`, `pages/`, `partials/macros.html`, `seo/`) |
| Styles and scripts | `app/static/css/site.css` (tokens at the top), `app/static/js/` |
| Images | `app/static/img/`; originals and other brand files in `docs/brand/` (not shipped) |
| Articles and videos | `content/resources/*.md`, `content/videos/*.md` (see `content/README.md`) |
| Settings | `.env`, documented in `.env.example`; read in `app/config.py` |
| Docker, Caddy, compose, the server's deploy script | `docker/` (`deploy.sh` runs on the server) |
| CI and releases | `.github/workflows/ci.yml` (checks on every PR), `release.yml` (on a version tag) |
| Tests | `tests/test_site.py` |

## Keep it simple

The owner wants **one of everything**: one `.env`, one compose file (`docker/compose.yml`), one `requirements.txt`, one live environment (no test site). Extend what exists instead of adding parallel files, environments or tools. Ask before adding a dependency or a new service.

## Settings

- One `.env`, the same file on the PC and the server (`~/ronsystemsai/docker/.env`). Never commit it.
- Never put `APP_ENV` or `SITE_URL` in `.env`. The PC defaults to development; `docker/compose.yml` sets production, and `SITE_URL` follows from `APP_ENV`.
- Keep comments on their own lines in `.env` files. Docker Compose reads `KEY=   # note` as the value.

## Content rules

- Plain business English, US spelling, outcome first. The reader isn't technical.
- **Never fabricate:** testimonials, client names or logos, quantified results, photos of Ron, or tools and experience he hasn't confirmed. Omit rather than invent.
- **No prices, no time-zone or availability promises, no client-location claims** in visible copy. Tests check prices and time-zone wording on every page.
- Ron's background: present it by industries and strengths ("11+ years across finance, healthcare, manufacturing, IT service providers (MSPs) and startups"). No dated job timeline, job titles or degree.
- Tools named on the site are **examples, not a complete list**: say Ron works with what the client already uses and recommends when they're starting fresh.
- The discovery call is a **free 30-minute phone call** booked through a Proton Calendar page (`BOOKING_URL`). There's **no contact form** by decision; `/contact/` redirects to `/book/`.
- When copy about Ron or the services changes, update `app/templates/seo/llms.txt` and the JSON-LD in `schema.py` to match.

## Search and AI visibility rules

These are checked by tests; keep them passing.

- All main content in the server-rendered HTML. Never load content with client-side JavaScript.
- Exactly one `<h1>` per page. `<title>` at most 60 characters, meta description at most 155.
- Every page URL ends with `/`; Flask redirects the other form. Keep canonical tags self-referencing.
- Sitemap `<lastmod>` only for real dates (Markdown items). Never "today".
- **No cookies** anywhere: the privacy page promises it. **No inline `style=` attributes**: the Content-Security-Policy blocks them.
- Non-production environments are `noindex`; empty listings are `noindex`.
- Images: size them for the web (about 2x the displayed size, WebP for photos), and keep originals out of `app/static/`.

## Design rules

Follow [DESIGN.md](DESIGN.md). Colors are CSS custom properties at the top of `site.css`; don't hard-code new hex values. Red is reserved for the main action and "this now runs by itself"; emphasis is reversed printing (white on ink), not a new color.

## Git and deploy

- Long-lived branches: `main` (releases) and `dev` (finished work). **Never push to either directly.** Branch from `dev` (`feature/`, `fix/`, `content/`; `hotfix/` from `main`) and open a PR; see [docs/10-git-workflow.md](docs/10-git-workflow.md).
- Nothing deploys automatically. A `vX.Y.Z` tag on `main` builds the image and the GitHub release; Ron runs `docker/deploy.sh <version>` on the server. **Never create tags or releases, or touch the server, unless asked.**
- CI (the `checks` job) must stay green: it lints, tests, validates `docker/compose.yml`, builds the image and loads pages from it.
- Commit only when asked. Commit messages: `type: short description` (`feat`, `fix`, `content`, `style`, `docs`, `chore`, `refactor`, `test`).
- Record notable decisions in [docs/08-open-decisions.md](docs/08-open-decisions.md) and keep the README and docs in step with code changes.
