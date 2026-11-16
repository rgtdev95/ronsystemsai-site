# 13 — Releasing and deploying (step by step)

How a change gets from `dev` to the live site. The branch rules are in [10-git-workflow.md](10-git-workflow.md), and the reasons in decision 18 ([08-open-decisions.md](08-open-decisions.md)).

```text
dev ──PR (merge commit)──► main ──git tag v1.2.0──► GitHub: checks → image → release
                                                                   │
                                     on the server: ./deploy.sh v1.2.0
                                                                   ▼
                                                           ronsystemsai.com
```

Nothing deploys by itself. GitHub builds each release, and you put it on the server with one command.

> **For now (decision 19):** GitHub Actions can't run on this account until a billing lock is cleared. CI is paused, so run `uv run ruff check app tests wsgi.py` and `uv run pytest -q` before merging. In step 2, leave **Require status checks to pass** off, or every PR stays blocked waiting for a `checks` status that never comes. Step 5 (the Release workflow) can't run either, so the first release waits until the lock is cleared.

- [First release (one time)](#first-release-one-time)
- [Every release after that](#every-release-after-that)
- [Hotfix](#hotfix) · [Rollback](#rollback) · [Version numbers](#version-numbers)
- [On the server](#on-the-server) · [When something goes wrong](#when-something-goes-wrong)

## First release (one time)

Do these in order. Steps 1–6 happen on GitHub and your PC, and steps 7–11 on the server. The site is down for a few minutes between steps 8 and 10.

### 1. Get the work into `dev`

Open a pull request from your branch (the first time: `feature/launch-prep`) into **`dev`**. GitHub shows a "Compare & pull request" banner after a push. Wait for the **checks** to go green, then **Squash and merge** and delete the branch.

### 2. GitHub settings

You can only add the `checks` status once CI has run once, which step 1 did.

- **Settings → Rules → Rulesets → New branch ruleset**
  - Name: `main and dev`. Enforcement: **Active**
  - Target branches: add `main` and `dev`
  - Turn on: **Restrict deletions**, **Require a pull request before merging** (required approvals: **0**, since you can't approve your own PR), **Require status checks to pass** (add **`checks`**), **Block force pushes**
- **Settings → General → Default branch:** `dev`, so new PRs target it
- **Settings → Secrets and variables → Actions:** delete `VPS_HOST`, `VPS_USER` and `VPS_SSH_KEY`. Nothing in GitHub reaches the server anymore
- **Settings → Environments:** delete `prod`

### 3. The release pull request

Open a pull request with base **`main`** and compare **`dev`**, titled `Release v1.0.0`. Wait for green, then **Create a merge commit** (not squash).

### 4. Tag the release

On your PC:

```bash
git switch main && git pull
git tag v1.0.0 && git push origin v1.0.0
```

### 5. Wait for the release

On GitHub, open **Actions → Release** and wait for green (about 3 minutes). **v1.0.0** then shows on the repo's **Releases** page, with the merged PRs and the deploy command.

### 6. Make the image public

Your GitHub profile → **Packages** → `ronsystemsai-site` → **Package settings** → **Change visibility** → **Public**. The server can't download the image otherwise. The repo is public already, so this reveals nothing new.

### 7. Check the server has what it needs

```bash
ssh <user>@<server>
git --version && docker compose version && curl --version | head -1
```

All three should print a version. If `docker compose` isn't found, install Docker's Compose plugin.

### 8. Stop the old site and get a fresh copy of the repo

The old containers hold ports 80 and 443, so they have to stop first.

```bash
docker ps --format '{{.Names}}\t{{.Image}}'   # find the site's containers: Caddy, the website, Umami, PostgreSQL
docker stop <name> <name> ...                 # stop those
mv ~/ronsystemsai ~/ronsystemsai-old          # keep the old folder until the new one works
git clone https://github.com/rgtdev95/ronsystemsai-site.git ~/ronsystemsai
exit
```

### 9. Copy your `.env` to the server

From the project folder on your PC:

```bash
scp .env <user>@<server>:~/ronsystemsai/docker/.env
```

### 10. Deploy

```bash
ssh <user>@<server>
cd ~/ronsystemsai/docker
grep -E '^UMAMI_(DB_PASSWORD|APP_SECRET)=' .env   # both need values
./deploy.sh v1.0.0
```

If either Umami value is empty, generate one with `python3 -c "import secrets; print(secrets.token_hex(32))"`, add it to `.env`, and keep it from then on. Umami starts with a fresh database: it wasn't recording visits yet, and its old data stays in the old `deploy_*` volumes.

The script ends with `==> Live: v1.0.0 at https://ronsystemsai.com`. The first start takes a minute longer while Caddy gets new HTTPS certificates.

### 11. Check the site and set up Umami

- Open https://ronsystemsai.com and click through a few pages
- Open https://stats.ronsystemsai.com and log in with `admin` / `umami`. **Change the password straight away**, then **Add website** (`ronsystemsai.com`)
- Copy the Website ID into `UMAMI_WEBSITE_ID`, in your PC's `.env` and the server's. Then run `docker compose up -d` on the server (in `~/ronsystemsai/docker`) so the site picks it up

### 12. Clean up the old setup

Once everything works:

- Copy anything you still want out of `~/ronsystemsai-old` (old `.env.*` files), then `rm -rf ~/ronsystemsai-old`
- `docker container prune` removes the stopped old containers
- `docker volume ls`, then `docker volume rm` each old `deploy_...` volume
- Revoke the Proton SMTP token, if you ever created one
- Optional: delete the `test` DNS record (the test site is gone)

## Every release after that

1. **PR `dev` → `main`**, titled `Release v1.2.0`. Wait for green, then **Create a merge commit**.
2. **Tag** on your PC:

   ```bash
   git switch main && git pull
   git tag v1.2.0 && git push origin v1.2.0
   ```

3. **Wait** for **Actions → Release** to go green.
4. **Deploy:** `ssh` to the server, then:

   ```bash
   cd ~/ronsystemsai/docker && ./deploy.sh v1.2.0
   ```

5. **Check** https://ronsystemsai.com.

Tag from the command line, not with GitHub's "Draft a new release" button. The workflow creates the release itself, once the image is pushed.

## Hotfix

For an urgent fix that can't wait for what's in `dev`:

1. `git switch main && git pull && git switch -c hotfix/<name>`. Fix it, commit, push
2. PR `hotfix/<name>` → **`main`**. Wait for green, merge
3. Tag the next patch version (e.g. `v1.2.1`), wait for the release, deploy, the same as steps 2–5 above
4. PR **`main` → `dev`** with a merge commit, so `dev` has the fix too

## Rollback

Run the deploy command with the previous version:

```bash
cd ~/ronsystemsai/docker && ./deploy.sh v1.1.0
```

That puts back that release's image, `compose.yml` and `Caddyfile`. Then fix the problem on a branch and release a new version as usual. Don't delete or move the bad tag.

## Version numbers

`vMAJOR.MINOR.PATCH`, always with the `v`:

| Change | Bump | Example |
|---|---|---|
| Fixes, copy edits | Patch | `v1.2.0` → `v1.2.1` |
| New pages, sections, articles, case studies | Minor | `v1.2.1` → `v1.3.0` |
| A redesign or a big restructure | Major | `v1.3.0` → `v2.0.0` |

`v1.0.0` is the public launch.

## On the server

Run these in `~/ronsystemsai/docker`.

| To | Run |
|---|---|
| Deploy or roll back | `./deploy.sh v1.2.0` |
| See which version is live | `grep IMAGE_TAG .env` |
| See what's running | `docker compose ps` |
| Read the logs | `docker compose logs -f web` (or `caddy`, `umami`) |
| Apply a `.env` change | `docker compose up -d` (keeps the same version) |
| Update Caddy, Umami and PostgreSQL every month or so | `docker compose pull && docker compose up -d` |

Don't edit `compose.yml` or the `Caddyfile` on the server. Change them in the repo and release, because the next deploy replaces them with the release's copies.

## When something goes wrong

| What you see | What to do |
|---|---|
| A PR's **checks** fail | Open the run in the PR and read the failed step. Fix it on the same branch and push; the checks run again |
| **Release** fails at "Check the tag is on main" | The tag isn't on `main`. Delete it with `git tag -d v1.2.0 && git push origin :refs/tags/v1.2.0`, merge into `main` first, then tag again |
| **Release** fails in the checks | Delete the tag as above, fix it through a PR into `dev` and a new release PR, then tag again |
| **Release** fails at "Create the GitHub release" | The image is already pushed. Click **Re-run failed jobs** on the run |
| `./deploy.sh: Permission denied` | Run it as `sh deploy.sh v1.2.0` |
| `manifest unknown` or `pull access denied` | The Release workflow hasn't finished, the version is mistyped, or the image is still private (step 6) |
| `Your local changes ... would be overwritten by checkout` | Someone edited a file on the server. `git status` shows which. `git checkout -- <file>` throws the edits away (your `.env` is safe: git ignores it). Then run the deploy again |
| `healthz isn't answering` | `docker compose ps` and `docker compose logs caddy web`. Common causes: old containers still holding ports 80/443 (`docker ps`), or DNS not pointing at the server |
