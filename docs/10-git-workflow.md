# 10 — Git workflow and releases

A simple git flow with two long-lived branches, `main` and `dev`. Nothing deploys by itself. A release is a version tag on `main`, created with a release on GitHub. The tag makes GitHub build the image, and you put that release on the server with one command (decisions 18 and 23 in [08-open-decisions.md](08-open-decisions.md)).

```text
feature/*  ┐
fix/*      ├─PR─►  dev  ──PR──►  main  ──release v1.2.0──►  GitHub release + image
content/*  ┘       (CI)          (CI)                         │
                                  ▲                            ▼  sudo ./deploy.sh v1.2.0 (by hand)
hotfix/*  ──PR─────────────────────┘                     ronsystemsai.com
          (then PR main → dev)
```

## Where each step happens

| Where | What you do there |
|---|---|
| **Your PC** (git in the terminal) | Start a branch, commit, run the lint and tests, push the branch. While GitHub Actions is blocked, also build and push the release image ([13-releasing.md](13-releasing.md#build-and-push-the-image-by-hand)) |
| **GitHub's website** | Open and merge pull requests, delete merged branches, and create releases. The release form also creates the version tag |
| **The VPS** | Deploy: `sudo ./deploy.sh <version>` |

Git on your PC never writes to `dev` or `main`. GitHub refuses a direct push to either ("Changes must be made through a pull request"), so everything reaches them through a pull request.

## Branches

| Branch | Lives | What it holds | Gets changes from |
|---|---|---|---|
| `main` | always | Released code. Every release is a tag on it | A PR from `dev`, or from `hotfix/*` |
| `dev` | always | Finished work waiting for the next release | PRs from the short-lived branches below |
| `feature/<name>` | until merged | New pages, sections, features | Branch from `dev`, PR into `dev` |
| `fix/<name>` | until merged | Bug fixes, small changes, docs | Same |
| `content/<name>` | until merged | Articles, videos, case studies | Same |
| `hotfix/<name>` | until merged | An urgent fix to the live site | Branch from `main`, PR into `main`; afterwards PR `main` → `dev` |

Delete short-lived branches once they're merged: **Delete branch** on the merged PR for GitHub's copy, and step 6 of [Day to day](#day-to-day) for your PC's.

GitHub's active `main and dev` ruleset enforces pull requests and blocks deletion and force pushes on both branches, with zero required review approvals. Required status checks stay off while CI is paused (decision 19).

## What runs on GitHub

| When | Workflow | What it does |
|---|---|---|
| A pull request into `dev` or `main` | **CI** (`.github/workflows/ci.yml`) | The checks below. **Paused for now** (decision 19): run the lint and tests locally before merging |
| A tag like `v1.2.0` is created (publishing a release on GitHub creates it) | **Release** (`.github/workflows/release.yml`) | The same checks, then: checks the tag is on `main` → builds the image and pushes it to `ghcr.io/rgtdev95/ronsystemsai-site:v1.2.0` and `:latest` → creates the GitHub release if it doesn't exist yet. **Blocked for now** (decision 19): build and push the image by hand ([13-releasing.md](13-releasing.md#build-and-push-the-image-by-hand)) |
| A push or merge to `dev` or `main` | nothing | The PR was already checked |

The CI checks, in order:

1. **Lint** (ruff): code mistakes and unused imports
2. **Tests** (pytest): every page renders, with one `<h1>`, a title and description within length and a correct canonical URL. No prices, time zones or cookies. Sitemap, robots.txt, llms.txt and structured data are right
3. **Compose file check**: `docker/compose.yml` is valid, so a typo there can't reach the server
4. **Image build**: the Dockerfile still builds
5. **Smoke test**: starts the image the way the server runs it (production settings, read-only) and loads the home, services, about and booking pages, robots.txt, the sitemap and llms.txt. This stands in for a test server. It catches what the tests can't see, like a file missing from the image or Gunicorn failing to start

If you get a dev server later, the natural next step is a `dev` image (`:dev`) pushed on every merge to `dev` and run there.

## Day to day

1. **Start a branch from the latest `dev`** (PC):

   ```bash
   git switch dev && git pull
   git switch -c feature/case-study-pages
   ```

   Start it this way, not from `origin/dev` in VS Code's branch menu. A branch made from `origin/dev` syncs with `dev`, so VS Code's **Sync** button tries to push straight into `dev` and GitHub refuses it.

2. **Work and commit** (PC). Check your change in the browser with `uv run flask --app wsgi run --debug`, then:

   ```bash
   git status
   git add -A
   git commit -m "feat: add case study pages"
   ```

   `git status` lists what's about to go in. `.env`, drafts and `docs/about-ron/` are ignored, so they never show up there. Commit as often as you like; the merge in step 5 turns them into one commit.

3. **Check and push** (PC):

   ```bash
   uv run ruff check app tests wsgi.py
   uv run pytest -q
   git push -u origin feature/case-study-pages
   ```

   The `-u` on the first push makes the branch sync with its own copy on GitHub. After that, `git push` (or VS Code's **Sync**) is enough.

4. **Open the pull request** (GitHub). On the repo page, click **Compare & pull request** in the yellow banner, or go to **Pull requests → New pull request**. Set **base: `dev`** and **compare:** your branch. Title it like a commit message (`feat: add case study pages`), then **Create pull request**.

5. **Merge it** (GitHub). Make sure the green button says **Squash and merge**; if it doesn't, pick it from the arrow next to it. Check the commit message in the box, **Confirm squash and merge**, then **Delete branch**.

6. **Tidy up** (PC):

   ```bash
   git switch dev && git pull
   git branch -D feature/case-study-pages
   git fetch --prune
   ```

   It's `-D`, not `-d`: after a squash merge, git can't tell the branch was merged, so `-d` refuses to delete it. `git fetch --prune` drops your PC's record of branches deleted on GitHub.

## Releasing

In short, on GitHub: a PR from `dev` into `main` (merge commit), then a release that creates the version tag on `main`. Then the image (built on your PC while Actions is blocked), and `sudo ./deploy.sh <version>` on the server. The full steps, including the first-time setup, hotfixes, rollbacks and version numbers, are in [13-releasing.md](13-releasing.md).

## Conventions

- **Commit messages:** `type: short description`, where type is `feat`, `fix`, `content`, `style`, `docs`, `chore`, `refactor`, or `test`.
  Example: `content: add n8n vs Zapier article`. When GitHub squash-merges a PR, the commit on `dev` uses the PR's title (or the commit's, if the PR has only one), so give PRs titles in the same form.
- **Merge style:** squash-merge short-lived branches into `dev` (one commit per change). Use a merge commit for `dev` → `main` and `main` → `dev`, so releases are easy to see and the branches stay in step. GitHub remembers the last method you used, so read the button before you click: **Squash and merge** into `dev`, **Create a merge commit** into `main`. A squashed release PR leaves `main` and `dev` with different histories, and the next release PR shows conflicts ([the fix](13-releasing.md#fix-a-squash-merged-release-pr)).
- **Never commit:** `.env` (only `.env.example`), `docs/about-ron/`, secrets, or client data.

## GitHub settings

The `main and dev` ruleset (add the `checks` status only once CI runs again), `dev` as the default branch (so new PRs start with base `dev`), the image's visibility and removing the old server secrets: step 2 and step 6 of [13-releasing.md](13-releasing.md#first-release-one-time).
