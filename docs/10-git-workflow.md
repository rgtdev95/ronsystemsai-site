# 10 — Git workflow and releases

A simple git flow with two long-lived branches, `main` and `dev`. Nothing deploys by itself. A release is a version tag on `main`. The tag makes GitHub build the image and publish a release, and you put that release on the server with one command (decision 18 in [08-open-decisions.md](08-open-decisions.md)).

```text
feature/*  ┐
fix/*      ├─PR─►  dev  ──PR──►  main  ──tag v1.2.0──►  GitHub release + image
content/*  ┘       (CI)          (CI)                         │
                                  ▲                            ▼  ./deploy.sh v1.2.0 (by hand)
hotfix/*  ──PR─────────────────────┘                     ronsystemsai.com
          (then PR main → dev)
```

## Branches

| Branch | Lives | What it holds | Gets changes from |
|---|---|---|---|
| `main` | always | Released code. Every release is a tag on it | A PR from `dev`, or from `hotfix/*` |
| `dev` | always | Finished work waiting for the next release | PRs from the short-lived branches below |
| `feature/<name>` | until merged | New pages, sections, features | Branch from `dev`, PR into `dev` |
| `fix/<name>` | until merged | Bug fixes, small changes, docs | Same |
| `content/<name>` | until merged | Articles, videos, case studies | Same |
| `hotfix/<name>` | until merged | An urgent fix to the live site | Branch from `main`, PR into `main`; afterwards PR `main` → `dev` |

Delete short-lived branches once they're merged (the button on the PR, or `git branch -d <name>` locally).

## What runs on GitHub

| When | Workflow | What it does |
|---|---|---|
| A pull request into `dev` or `main` | **CI** (`.github/workflows/ci.yml`) | The checks below. **Paused for now** (decision 19): run the lint and tests locally before merging |
| You push a tag like `v1.2.0` | **Release** (`.github/workflows/release.yml`) | The same checks, then: checks the tag is on `main` → builds the image and pushes it to `ghcr.io/rgtdev95/ronsystemsai-site:v1.2.0` and `:latest` → creates the GitHub release, with the merged PRs listed and the deploy command |
| A push or merge to `dev` or `main` | nothing | The PR was already checked |

The CI checks, in order:

1. **Lint** (ruff): code mistakes and unused imports
2. **Tests** (pytest): every page renders, with one `<h1>`, a title and description within length and a correct canonical URL. No prices, time zones or cookies. Sitemap, robots.txt, llms.txt and structured data are right
3. **Compose file check**: `docker/compose.yml` is valid, so a typo there can't reach the server
4. **Image build**: the Dockerfile still builds
5. **Smoke test**: starts the image the way the server runs it (production settings, read-only) and loads the home, services, about and booking pages, robots.txt, the sitemap and llms.txt. This stands in for a test server. It catches what the tests can't see, like a file missing from the image or Gunicorn failing to start

If you get a dev server later, the natural next step is a `dev` image (`:dev`) pushed on every merge to `dev` and run there.

## Day to day

```bash
git switch dev && git pull
git switch -c feature/case-study-pages

# ...commit as you go, and check it on your PC: uv run flask --app wsgi run --debug
git push -u origin feature/case-study-pages
# open a PR into dev; CI runs; squash-merge; delete the branch
```

## Releasing

In short: a PR from `dev` into `main` (merge commit), a version tag on `main`, a wait for the Release workflow, then `./deploy.sh <version>` on the server. The full steps, including the first-time setup, hotfixes, rollbacks and version numbers, are in [13-releasing.md](13-releasing.md).

## Conventions

- **Commit messages:** `type: short description`, where type is `feat`, `fix`, `content`, `style`, `docs`, `chore`, `refactor`, or `test`.
  Example: `content: add n8n vs Zapier article`
- **Merge style:** squash-merge short-lived branches into `dev` (one commit per change). Use a merge commit for `dev` → `main` and `main` → `dev`, so releases are easy to see and the branches stay in step.
- **Never commit:** `.env` (only `.env.example`), `docs/about-ron/`, secrets, or client data.

## GitHub settings

Branch protection for `main` and `dev` (requiring the `checks` status), `dev` as the default branch, the image's visibility and removing the old server secrets: step 2 and step 6 of [13-releasing.md](13-releasing.md#first-release-one-time).
