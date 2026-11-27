# personal-site

Website for **Ron Systems AI** ([ronsystemsai.com](https://ronsystemsai.com)): IT systems, automation, and AI consulting for small and medium businesses in English-speaking markets, by Rolando "Ron" Tactay.

## Project map

```
personal-site/
├── README.md                     ← you are here
├── AGENTS.md                     ← instructions for AI coding agents (Codex, Claude Code)
├── PRODUCT.md                    ← one-page product summary (used by design tooling)
├── .gitignore                    ← keeps the resume, secrets, and Python caches out of git
├── app/                          ← Flask app (routes, templates, static, content data)
├── content/                      ← Markdown articles and videos
├── docker/                       ← Dockerfile, compose.yml (the one compose file: the website container), deploy.sh
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
    ├── 13-releasing.md           ← step by step: first release, every release, hotfix, rollback
    ├── about-ron/                ← private resume (gitignored)
    └── site-initial-design/      ← first design prototype (reference only)
```

## Stack at a glance

Flask + Jinja2 (server-rendered) · plain HTML/CSS/JS · Markdown content · Docker · VPS · Caddy · Umami

One live site, ronsystemsai.com, running releases tagged on `main`. There's no test site for now; check changes on your PC.

## Settings: one `.env` file

Copy `.env.example` to `.env` and fill it in. Don't put `APP_ENV` or `SITE_URL` in it: your PC is always development and the server is always production. The same file goes to the server at `/opt/apps/website/docker/.env` (root-only). On the VPS the site runs behind the VPS's shared Caddy and uses its Umami ([decision 21](docs/08-open-decisions.md)); releasing and deploying: [docs/13-releasing.md](docs/13-releasing.md).

## Run it locally

Uses [uv](https://docs.astral.sh/uv/) to manage the virtual environment. Python 3.12 matches the Docker image and CI.

```bash
uv venv --python 3.12                        # creates .venv (uv downloads 3.12 if needed)
uv pip install -r requirements.txt           # rerun after requirements.txt changes
uv run flask --app wsgi run --debug          # http://127.0.0.1:5000, reads .env automatically
uv run pytest -q                             # tests
uv run ruff check app tests wsgi.py          # lint
```

The deployment-script tests need a POSIX `sh` (available in Linux CI). Pytest skips those checks on a PC without it.

The Docker image upgrades pip from its pin in `requirements.txt` before installing the remaining packages.

## Branches, releases and deploys

Work goes from short-lived branches into `dev`, and from `dev` into `main`. You commit and push your branch with git on your PC, and open and merge pull requests and create releases on GitHub's website ([decision 23](docs/08-open-decisions.md)). CI checks every pull request (paused for now: [decision 19](docs/08-open-decisions.md)). To release, merge `dev` into `main`, then publish a release on GitHub with a new tag such as `v1.2.0` on `main`. GitHub then builds the image (on your PC, by hand, while Actions is blocked). Deploy it on the VPS with `cd /opt/apps/website/docker && sudo ./deploy.sh v1.2.0`. Step by step: [docs/13-releasing.md](docs/13-releasing.md).

The website container is defined in [docker/compose.yml](docker/compose.yml). Shared Caddy and Umami are managed in the VPS configuration repository (decision 21).

## Where things live

| What | Where |
|---|---|
| Page copy (services, process, FAQs) | `app/site_content.py` |
| Articles and videos | `content/resources/*.md`, `content/videos/*.md` (see `content/README.md`) |
| Templates | `app/templates/` |
| Styles / scripts | `app/static/css/site.css`, `app/static/js/site.js` |
| SEO: robots, sitemap, llms.txt, structured data | `app/routes/seo.py`, `app/services/schema.py` |
| Settings (booking link, email, Umami, social links) | environment variables, see `.env.example` |
| Deployment (Caddy, Umami, the website) | `docker/compose.yml`, `docker/deploy.sh`, `.github/workflows/` |
