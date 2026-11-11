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
| A pull request into `dev` or `main` | **CI** (`.github/workflows/ci.yml`) | The checks below |
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

1. Open a PR from `dev` into `main`, titled like "Release v1.2.0". CI runs again. Merge it with a **merge commit**.
2. Tag `main` and push the tag:

   ```bash
   git switch main && git pull
   git tag v1.2.0 && git push origin v1.2.0
   ```

3. On GitHub, open **Actions → Release** and wait for green (about 3 minutes). The release then shows on the repo's **Releases** page.
4. Put it on the server: `ssh` in, then `cd ~/ronsystemsai/docker && ./deploy.sh v1.2.0` (details in [09-architecture-and-deployment.md](09-architecture-and-deployment.md#releases-and-deploys)). To roll back, run the same command with the previous version.

Release from the command line, not GitHub's "Draft a new release" button: the workflow creates the release itself, after the image is pushed.

**Versions** are `vMAJOR.MINOR.PATCH`:

- **Patch** (`v1.2.1`): fixes and copy edits
- **Minor** (`v1.3.0`): new pages, sections, articles, case studies
- **Major** (`v2.0.0`): a redesign or a big restructure

`v1.0.0` is the public launch.

**Hotfix:** branch `hotfix/<name>` from `main`, PR into `main`, merge, tag a patch version, deploy. Then open a PR from `main` into `dev` so `dev` has the fix too.

## Conventions

- **Commit messages:** `type: short description`, where type is `feat`, `fix`, `content`, `style`, `docs`, `chore`, `refactor`, or `test`.
  Example: `content: add n8n vs Zapier article`
- **Merge style:** squash-merge short-lived branches into `dev` (one commit per change). Use a merge commit for `dev` → `main` and `main` → `dev`, so releases are easy to see and the branches stay in step.
- **Never commit:** `.env` (only `.env.example`), `docs/about-ron/`, secrets, or client data.

## GitHub settings to turn on

- **Branch protection** for `main` and `dev` (Settings → Branches → Add branch ruleset, or a classic rule):
  - require a pull request before merging, with **0 approvals** (you can't approve your own PR)
  - require the **`checks`** status check to pass. It appears in the list after CI has run once
  - block force pushes and deletion
- **Default branch: `dev`** (Settings → General), so new PRs target it.
- **Image visibility:** after the first release, open the `ronsystemsai-site` package (your GitHub profile → Packages → Package settings → Change visibility) and make it **public**, so the server can pull it without a login. The repo is public already, so this reveals nothing new. To keep it private instead, run `docker login ghcr.io` once on the server with a token that has `read:packages`.
- **No repository secrets are needed.** The workflows use GitHub's built-in token. Delete the old `VPS_HOST`, `VPS_USER` and `VPS_SSH_KEY` secrets and the `prod` environment (Settings → Secrets and variables → Actions; Settings → Environments).
