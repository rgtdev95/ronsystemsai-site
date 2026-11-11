# 09 — Architecture and deployment

## Stack

| Layer | Choice | Why |
|---|---|---|
| Backend | **Flask** (Python 3.12) | Familiar, small, and enough for a content site |
| Templates | **Jinja2**, server-rendered | Every page arrives as complete HTML, which search engines and AI crawlers can read without running JavaScript |
| Styling | **Plain CSS** (custom properties / design tokens, no framework) | Full control of the look; no build step |
| Interactivity | **Plain JavaScript**, progressive enhancement only | Content and navigation work without JS; JS adds the diagram animation, process stepper, theme toggle, and mobile menu |
| Content | **Markdown files with front-matter** for articles, videos, and case studies | Writing a new article = adding one `.md` file. No database needed |
| App server | **Gunicorn** inside the container | Production WSGI server |
| Container | **Docker** + **Docker Compose** | Same image runs in test and prod |
| Reverse proxy / TLS | **Caddy** (decided) | Automatic HTTPS certificates, compression, security headers, routes both environments by hostname |
| Hosting | Own **VPS** | Both environments on one VPS to start |
| Analytics | **Umami** (self-hosted container on the same VPS, with its own PostgreSQL) | Cookie-less; served from `stats.ronsystemsai.com` |

No database for launch, and no contact form: visitors book a call or email directly (decision 16 in [08-open-decisions.md](08-open-decisions.md)). Add SQLite or PostgreSQL only when something actually needs storage.

## Planned project layout

```
personal-site/
├── app/
│   ├── __init__.py            # create_app() factory, loads config by APP_ENV
│   ├── config.py              # BaseConfig / TestConfig / ProductionConfig
│   ├── routes/
│   │   ├── pages.py           # home, services, work, process, about, faq, book, legal (/contact/ redirects to /book/)
│   │   ├── content.py         # /resources/<slug>, /videos/<slug>, /work/<slug>
│   │   └── seo.py             # sitemap.xml, robots.txt, llms.txt, security.txt
│   ├── services/
│   │   ├── content_loader.py  # reads Markdown + front-matter, caches
│   │   └── schema.py          # builds JSON-LD structured data
│   ├── templates/
│   │   ├── base.html          # <head>, meta, OG tags, JSON-LD, header/footer
│   │   ├── partials/
│   │   └── pages/
│   └── static/
│       ├── css/
│       ├── js/
│       ├── img/
│       └── fonts/             # self-hosted fonts (faster, no third-party requests)
├── content/
│   ├── resources/*.md
│   ├── videos/*.md
│   └── work/*.md
├── tests/                     # pytest: routes return 200, sitemap valid, noindex on test, etc.
├── docker/                    # everything Docker
│   ├── Dockerfile             # the website image (build from the project root: docker build -f docker/Dockerfile .)
│   ├── Dockerfile.dockerignore  # what stays out of the image
│   ├── compose.yml            # the one compose file: Caddy + website + Umami
│   ├── Caddyfile
│   └── deploy.sh              # run on the server: ./deploy.sh v1.2.0
├── requirements.txt
├── .env.example               # the one settings file (copy to .env), no secrets
├── .github/workflows/         # ci.yml (checks) + release.yml (see below)
├── docs/                      # planning (this folder)
│   ├── about-ron/             # private resume, gitignored
│   └── site-initial-design/   # design reference
```

## Environments

One environment for now: the live site. You develop and check changes on your own PC. A separate test site was planned but dropped on 2026-11-08 to keep things simple (decision 17 in [08-open-decisions.md](08-open-decisions.md)).

| | **Your PC** | **Live** |
|---|---|---|
| URL | `http://127.0.0.1:5000` | `ronsystemsai.com` (+ `www` → redirect) |
| How it runs | `uv run flask --app wsgi run --debug` | `docker/compose.yml` on the VPS, running a release tagged on `main` |
| `APP_ENV` | `development` (the default) | `production` (set in `docker/compose.yml`) |
| Settings | `.env` in the project folder (loaded automatically) | `.env` next to `docker/compose.yml`: the same file, plus the Umami database values |
| Search indexing | — | Allowed, including AI crawlers |
| Analytics (Umami) | Off | On |

`APP_ENV` decides the site's address too (`SITE_URL`), so it never goes in `.env`. The code still supports `APP_ENV=test` (`test.ronsystemsai.com`, noindex) in case a test site comes back.

## How the containers run on the VPS

```
Internet ──► Caddy (ports 80/443, TLS)
               ├── www.ronsystemsai.com    ──► 301 redirect to ronsystemsai.com
               ├── ronsystemsai.com        ──► web       (gunicorn :8000, image :<version>)
               └── stats.ronsystemsai.com  ──► umami     (:3000) + umami-db (PostgreSQL, internal only)
```

- All four containers are defined in one file, `docker/compose.yml`. Caddy owns ports 80/443 and is the only container exposed to the internet; the others publish no ports on the host.
- Certificates: Caddy gets and renews Let's Encrypt certificates automatically. Keep its `/data` volume so certificates survive restarts. DNS A records for `@`, `www`, and `stats` point to the VPS.

### Caddyfile outline

```caddyfile
{
	email contactme@ronsystemsai.com
}

(security_headers) {
	header {
		Strict-Transport-Security "max-age=31536000; includeSubDomains"
		X-Content-Type-Options "nosniff"
		Referrer-Policy "strict-origin-when-cross-origin"
		Permissions-Policy "camera=(), microphone=(), geolocation=()"
		-Server
	}
}

www.ronsystemsai.com {
	redir https://ronsystemsai.com{uri} permanent
}

ronsystemsai.com {
	import security_headers
	encode zstd gzip
	reverse_proxy web:8000
}

stats.ronsystemsai.com {
	import security_headers
	encode zstd gzip
	reverse_proxy umami:3000
}
```

The Content-Security-Policy is set by Flask. Booking opens Proton Calendar in a new tab instead of embedding it, so no third-party booking script needs to be allowed.
- Secrets (`SECRET_KEY`, Umami's database password and app secret) live in `.env`, on your PC and on the VPS, never in git.
- Containers run as a non-root user, with `restart: unless-stopped` and a `/healthz` endpoint for health checks.

## Releases and deploys

Nothing deploys by itself. GitHub builds each release, and you put it on the server by hand (decision 18 in [08-open-decisions.md](08-open-decisions.md)). The branch flow is in [10-git-workflow.md](10-git-workflow.md).

| When | What happens |
|---|---|
| A pull request into `dev` or `main` | **CI**: lint → tests → compose file check → build the image → start it and load key pages. Nothing is published |
| You push a tag like `v1.2.0` on `main` | **Release**: the same checks → image pushed to `ghcr.io/rgtdev95/ronsystemsai-site:v1.2.0` and `:latest` → GitHub release with the merged PRs and the deploy command |
| You run `./deploy.sh v1.2.0` on the server | Checks out that tag, so `compose.yml` and the `Caddyfile` match the release → records `IMAGE_TAG=v1.2.0` in `.env` → pulls the image and restarts the site, waiting until it's healthy (a few seconds of downtime) → checks `https://ronsystemsai.com/healthz` → asks search engines to recrawl through IndexNow, if `INDEXNOW_KEY` is set |
| Rollback | The same command with an older version: `./deploy.sh v1.1.0` |

GitHub holds no server keys or secrets: the workflows only use GitHub's built-in token, and nothing in GitHub can reach the VPS.

### The server

`~/ronsystemsai` is a clone of the GitHub repo. The repo is public, so it needs no deploy key. The settings live in `~/ronsystemsai/docker/.env`: your PC's `.env` plus the server-only values at the end of `.env.example`. Set it up once:

```bash
git clone https://github.com/rgtdev95/ronsystemsai-site.git ~/ronsystemsai
cd ~/ronsystemsai/docker
nano .env                 # paste your PC's .env, then fill in the server-only values
./deploy.sh v1.0.0        # any released version
```

Handy commands, run in `~/ronsystemsai/docker`:

| To | Run |
|---|---|
| See which version is live | `grep IMAGE_TAG .env` |
| Read the logs | `docker compose logs -f web` (or `caddy`, `umami`) |
| Restart everything | `docker compose up -d` (keeps the version in `.env`) |
| Update Caddy, Umami and PostgreSQL every month or so | `docker compose pull && docker compose up -d` |

`compose.yml` fixes the Compose project name as `ronsystemsai`, so containers and volumes are named `ronsystemsai_*` whatever the folder is called. Keep the `ronsystemsai_caddy_data` and `ronsystemsai_umami_db` volumes: they hold the HTTPS certificates and Umami's data.

## Security and performance baseline

- Security headers: HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy (set in Caddy); Content-Security-Policy (set per page in Flask)
- No forms and no cookies, so there's nothing to protect with CSRF tokens or rate limiting. A test checks that no page sets a cookie
- `/.well-known/security.txt`
- Gzip/zstd compression and long cache headers for static files (cache-busting via file hash in the URL)
- Self-hosted fonts, optimized images (WebP/AVIF), no third-party scripts (booking links out to Proton Calendar)
- VPS: firewall (only 22/80/443), SSH keys only, automatic security updates, off-server backups of `.env` files and content
- Uptime monitoring for both URLs

## SEO/AEO/GEO hooks built into the app

- `base.html` renders the title, meta description, canonical URL, and Open Graph tags from each page's data
- `schema.py` produces JSON-LD for Organization/ProfessionalService, Person, Service, FAQPage, Article, VideoObject, and BreadcrumbList
- `seo.py` generates `sitemap.xml` from routes + Markdown content, and serves an environment-aware `robots.txt` and `llms.txt`
- Every Markdown item has `title`, `description`, `published`, `updated`, and `author` in its front-matter

See [05-search-and-ai-visibility.md](05-search-and-ai-visibility.md) for the full plan.
