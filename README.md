# personal-site

Website for **Ron Systems AI** ([ronsystemsai.com](https://ronsystemsai.com)): IT systems, automation, and AI consulting for small and medium businesses in English-speaking markets, by Rolando "Ron" Tactay.

## Project map

```
personal-site/
├── README.md                     ← you are here
├── PRODUCT.md                    ← one-page product summary (used by design tooling)
├── .gitignore                    ← keeps the resume, secrets, and Python caches out of git
├── app/                          ← Flask app (routes, templates, static, content data)
├── content/                      ← Markdown articles and videos
├── deploy/                       ← compose.yml (the one compose file) + Caddyfile for the VPS
├── tests/                        ← pytest
└── docs/                         ← planning: what the site is for and how it will work
    ├── 01-purpose-and-positioning.md
    ├── 02-audience-and-markets.md
    ├── 03-services.md            ← services in plain business language
    ├── 04-site-structure.md      ← sitemap, page templates, content backlog
    ├── 05-search-and-ai-visibility.md  ← SEO / AEO / GEO plan
    ├── 06-social-and-content.md  ← Facebook, YouTube, LinkedIn
    ├── 07-launch-checklist.md    ← domain, legal, payments, proof, tech launch
    ├── 08-open-decisions.md      ← decided + still-open choices
    ├── 09-architecture-and-deployment.md  ← Flask, Docker, VPS, CI/CD
    ├── 10-git-workflow.md        ← branches, releases, conventions
    ├── 11-case-studies.md        ← case study pages: plan, template, how to add one
    ├── 12-booking-follow-up.md   ← after a booking: manual email template + automation idea
    ├── about-ron/                ← private resume (gitignored)
    └── site-initial-design/      ← first design prototype (reference only)
```

## Stack at a glance

Flask + Jinja2 (server-rendered) · plain HTML/CSS/JS · Markdown content · Docker · VPS · Caddy · Umami

One live site, deployed from `main` to ronsystemsai.com. There's no test site for now; check changes on your PC.

## Settings: one `.env` file

Copy `.env.example` to `.env` and fill it in. The same file goes to the server at `~/ronsystemsai/deploy/.env`, plus the two Umami database values. Don't put `APP_ENV` or `SITE_URL` in it: your PC is always development and the server is always production.

## Run it locally

Uses [uv](https://docs.astral.sh/uv/) to manage the virtual environment. Python 3.12 matches the Docker image and CI.

```bash
uv venv --python 3.12                        # creates .venv (uv downloads 3.12 if needed)
uv pip install -r requirements-dev.txt       # rerun after requirements change
uv run flask --app wsgi run --debug          # http://127.0.0.1:5000, reads .env automatically
uv run pytest -q                             # tests
uv run ruff check app tests wsgi.py          # lint
```

## Deploy

Merging into `main` deploys automatically (`.github/workflows/deploy.yml`). Everything on the server is in one file, [deploy/compose.yml](deploy/compose.yml): Caddy, the website and Umami.

## Where things live

| What | Where |
|---|---|
| Page copy (services, process, FAQs, case studies) | `app/site_content.py` |
| Articles and videos | `content/resources/*.md`, `content/videos/*.md` (see `content/README.md`) |
| Templates | `app/templates/` |
| Styles / scripts | `app/static/css/site.css`, `app/static/js/site.js` |
| SEO: robots, sitemap, llms.txt, structured data | `app/routes/seo.py`, `app/services/schema.py` |
| Settings (booking link, email, Umami, social links) | environment variables, see `.env.example` |
| Deployment (Caddy, Umami, the website) | `deploy/compose.yml`, `.github/workflows/` |
