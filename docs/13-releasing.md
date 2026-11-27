# 13 — Releasing and deploying (step by step)

How a change gets from `dev` to the live site. The branch rules are in [10-git-workflow.md](10-git-workflow.md), and the reasons in decisions 18, 21 and 23 ([08-open-decisions.md](08-open-decisions.md)).

```text
dev ──PR (merge commit)──► main ──release v1.2.0──► GitHub release + image on ghcr.io
                                                                   │
                       on the VPS: cd /opt/apps/website/docker && sudo ./deploy.sh v1.2.0
                                                                   ▼
                                     VPS Caddy ──► website-ext-ovhvps1 ──► ronsystemsai.com
```

Nothing deploys by itself. On the VPS, only the website container comes from this repo: the VPS's shared Caddy serves `ronsystemsai.com` and `www`, and the site uses the VPS's shared Umami at `stats.ronsystemsai.com` (decision 21). Both are set up in the VPS configuration repo.

The pull requests and the release happen on GitHub's website. Git on your PC only pushes your own branches (decision 23; who does what is in [10-git-workflow.md](10-git-workflow.md#where-each-step-happens)).

`deploy.sh` accepts exactly one version in the form `vMAJOR.MINOR.PATCH`, with decimal numbers in all three parts. It rejects extra arguments, suffixes and other characters before reading `.env`, fetching tags or running Docker.

> **For now (decision 19):** GitHub Actions can't run on this account until a billing lock is cleared. CI is paused, so run `uv run ruff check app tests wsgi.py` and `uv run pytest -q` before merging, and leave **Require status checks to pass** off in the ruleset. The Release workflow can't build the image either, so build and push it from your PC: [Build and push the image by hand](#build-and-push-the-image-by-hand). Creating a tag still starts the Release workflow, and it fails straight away; that's expected until the lock is cleared.

- [First release (one time)](#first-release-one-time)
- [Every release after that](#every-release-after-that)
- [Build and push the image by hand](#build-and-push-the-image-by-hand)
- [Hotfix](#hotfix) · [Rollback](#rollback) · [Version numbers](#version-numbers)
- [On the server](#on-the-server) · [When something goes wrong](#when-something-goes-wrong) · [Fix: a squash-merged release PR](#fix-a-squash-merged-release-pr)

## First release (one time)

Steps 1–6 happen on GitHub and your PC, and steps 7–12 on the VPS and in Cloudflare. Nothing is live at `ronsystemsai.com` yet, so there's no downtime to plan around.

### 1. Get the work into `dev`

Push your branch, open a pull request into **`dev`** on GitHub, check `uv run ruff check app tests wsgi.py` and `uv run pytest -q` pass locally, then **Squash and merge** and delete the branch. Step by step: [Day to day](10-git-workflow.md#day-to-day).

### 2. GitHub settings

- **Settings → Rules → Rulesets → New branch ruleset**
  - Name: `main and dev`. Enforcement: **Active**
  - Target branches: add `main` and `dev`
  - Turn on: **Restrict deletions**, **Require a pull request before merging** (required approvals: **0**, since you can't approve your own PR), **Block force pushes**. Add **Require status checks to pass** (`checks`) only once CI runs again
- **Settings → General → Default branch:** `dev`, so new PRs target it
- **Settings → Secrets and variables → Actions:** delete `VPS_HOST`, `VPS_USER` and `VPS_SSH_KEY` if they're still there. Nothing in GitHub reaches the server
- **Settings → Environments:** delete `prod` if it's still there

### 3. The release pull request

On GitHub, a pull request with base **`main`** and compare **`dev`**, titled `Release v1.0.0`, merged with **Create a merge commit** (not squash): step 1 of [Every release after that](#every-release-after-that).

### 4. Create the release and its tag

On GitHub: step 2 of [Every release after that](#every-release-after-that), with `v1.0.0`.

### 5. Build and push the image

Follow [Build and push the image by hand](#build-and-push-the-image-by-hand) with `V=v1.0.0`.

### 6. Make the image public

Your GitHub profile → **Packages** → `ronsystemsai-site` → **Package settings** → **Change visibility** → **Public**. The VPS can't download the image otherwise. The repo is public already, so this reveals nothing new.

### 7. Add the website in Umami

Umami already runs on the VPS. With the Pangolin client connected, open its dashboard (`umami-ovhvps1` in Pangolin) → **Settings → Websites → Add website**: name `Ron Systems AI`, domain `ronsystemsai.com`. Copy its **Website ID** into `UMAMI_WEBSITE_ID` in your PC's `.env`, and check that `UMAMI_SCRIPT_URL=https://stats.ronsystemsai.com/script.js`. Do this before step 9, so the `.env` you copy to the VPS already has it.

### 8. DNS: point the domain at the VPS

Cloudflare → `ronsystemsai.com` → **DNS → Records**. Add two `A` records to the VPS's IPv4, both **DNS only** (grey cloud): name `@` and name `www`. Leave every Proton record (MX, SPF, DKIM, DMARC) and the `apps` NS records as they are.

Wait until both resolve, from PowerShell:

```powershell
Resolve-DnsName ronsystemsai.com -Server 1.1.1.1
Resolve-DnsName www.ronsystemsai.com -Server 1.1.1.1
```

Both should show the VPS's IP. This has to come before step 10: the zone's catch-all sends names without their own record elsewhere, and if Caddy asks Let's Encrypt for a certificate too early, it backs off for hours.

### 9. Get the site and its `.env` onto the VPS

```bash
ssh ovhvps
sudo docker ps --format '{{.Names}}'    # leftovers from the old deploy? (old site, Caddy or Umami containers from this repo)
sudo git clone https://github.com/rgtdev95/ronsystemsai-site.git /opt/apps/website
exit
```

If `docker ps` lists containers from the site's old setup, stop and remove those before step 11. **Never stop `caddy-ext-ovhvps1` or `umami-ext-ovhvps1`**: they're the VPS's shared Caddy and Umami, used by n8n, Outline and the analytics.

Then from the project folder on your PC (PowerShell is fine), copy your `.env` and lock it down:

```powershell
scp .env ovhvps:/tmp/ronsystemsai.env
ssh ovhvps "sudo install -m 600 -o root -g root /tmp/ronsystemsai.env /opt/apps/website/docker/.env && shred -u /tmp/ronsystemsai.env"
```

### 10. Route the domain to the site in the VPS's Caddy

In the VPS configuration repo, the Caddyfile's main-domain block sends `ronsystemsai.com` to `website-ext-ovhvps1:8000` with the security headers, and `www` redirects to it. Push that repo, then on the VPS follow its Caddy readme ("Change the Caddyfile"):

```bash
git -C ~/ovh-vps-homelab pull
sudo cp ~/ovh-vps-homelab/docker-apps/external/caddy/Caddyfile /opt/apps/caddy/
cd /opt/apps/caddy && sudo docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
sudo docker compose logs --since 5m caddy | grep -i -E "certificate|error"   # a certificate for ronsystemsai.com and www
```

If Caddy tried these names before the DNS records existed, it may be waiting out a back-off: `sudo docker compose restart caddy`. Until step 11, `https://ronsystemsai.com` answers 502. That's expected.

### 11. Deploy

```bash
ssh ovhvps
cd /opt/apps/website/docker
sudo grep -c -E '^(SECRET_KEY|UMAMI_WEBSITE_ID)=.' .env   # prints 2 when both have values (without showing them)
sudo ./deploy.sh v1.0.0
```

The script ends with `==> Live: v1.0.0 at https://ronsystemsai.com`.

### 12. Check

- Open https://ronsystemsai.com and `https://www.ronsystemsai.com` (should land on the first), and click through a few pages, both articles and `/resources/`
- Umami's dashboard shows your own visit within a minute
- https://securityheaders.com for `ronsystemsai.com`: HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy and the Content-Security-Policy
- Then the "After launch" items in [07-launch-checklist.md](07-launch-checklist.md): Search Console, Bing Webmaster Tools, Rich Results Test, PageSpeed Insights

## Every release after that

1. **Release PR** (GitHub): **Pull requests → New pull request**, base **`main`**, compare **`dev`**, titled `Release v1.2.0` → **Create pull request**. Lint and tests should pass on `dev` (on your PC: `git switch dev && git pull`, then `uv run ruff check app tests wsgi.py` and `uv run pytest -q`). Merge it with **Create a merge commit**; if the green button says anything else, pick it from the arrow next to it. Leave `dev` in place afterwards (the ruleset won't let it be deleted anyway).
2. **Release and tag** (GitHub): **Releases → Draft a new release**, then:
   - **Choose a tag:** type `v1.2.0` and pick **Create new tag: v1.2.0 on publish**. If the tag already exists, pick it from the list instead
   - **Target:** `main`. The form starts with the default branch, which is `dev`, so change it
   - **Release title:** `v1.2.0`
   - **Generate release notes**, and add this above them:

     ````markdown
     **Image:** `ghcr.io/rgtdev95/ronsystemsai-site:v1.2.0`

     **Deploy** on the VPS (the same command with an older version rolls back):

     ```
     cd /opt/apps/website/docker && sudo ./deploy.sh v1.2.0
     ```
     ````

   - **Publish release**. This creates the tag on `main`
3. **Image** (PC): [build and push it by hand](#build-and-push-the-image-by-hand) while Actions is blocked. Once Actions runs again, publishing the release starts **Actions → Release**, which builds and pushes the image; wait for it to go green instead.
4. **Deploy** on the VPS:

   ```bash
   cd /opt/apps/website/docker && sudo ./deploy.sh v1.2.0
   ```

5. **Check** https://ronsystemsai.com.

## Build and push the image by hand

What the Release workflow does, done on your PC. Run it in **Git Bash** (VS Code: the terminal's **+** menu → Git Bash), from the project folder, after you've published the release on GitHub (that creates the tag). Windows PowerShell 5.1 breaks the `git archive | docker build` pipe.

```bash
V=v1.0.0
IMAGE=ghcr.io/rgtdev95/ronsystemsai-site

# 1. Build from exactly the tagged code. git archive leaves out untracked files (.env, drafts),
#    and autocrlf=false keeps the repo's own line endings.
git fetch --tags
git merge-base --is-ancestor "$V" origin/main && echo "OK: $V is on main" || echo "STOP: $V isn't on main"
git -c core.autocrlf=false archive --format=tar "$V" | docker build -f docker/Dockerfile \
  --label "org.opencontainers.image.source=https://github.com/rgtdev95/ronsystemsai-site" \
  --label "org.opencontainers.image.version=$V" \
  --label "org.opencontainers.image.revision=$(git rev-parse "$V^{commit}")" \
  -t "$IMAGE:$V" -t "$IMAGE:latest" -

# 2. Start it the way the server does and load a few pages (what CI's smoke test does).
docker run -d --name site-check -p 8000:8000 --read-only --tmpfs /tmp \
  -e APP_ENV=production -e SECRET_KEY=check "$IMAGE:$V"
sleep 5
for path in /healthz / /services/ /resources/ /about/ /book/ /robots.txt /sitemap.xml /llms.txt; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:8000$path") $path"
done
docker rm -f site-check

# 3. Push it. The password is a GitHub token (classic) with only `write:packages`,
#    from GitHub → Settings → Developer settings → Personal access tokens.
docker login ghcr.io -u rgtdev95
docker push "$IMAGE:$V"
docker push "$IMAGE:latest"
```

The first check should say `OK`, and every line in step 2 should start with `200`. If not, don't push. `docker logs site-check` (before `docker rm`) shows why a page failed. The release page is already published by then, so open it on GitHub and **Delete** it (the tag stays), fix the problem through a PR into `dev`, and release the next patch version.

## Hotfix

For an urgent fix that can't wait for what's in `dev`:

1. **Branch from `main`** (PC): `git switch main && git pull && git switch -c hotfix/<name>`. Fix it, commit, and `git push -u origin hotfix/<name>`
2. **PR into `main`** (GitHub): base **`main`**, compare `hotfix/<name>`. **Squash and merge**, then **Delete branch**
3. **Release** the next patch version (e.g. `v1.2.1`), build and push the image, and deploy: steps 2–5 of [Every release after that](#every-release-after-that)
4. **PR `main` → `dev`** (GitHub): base **`dev`**, compare **`main`**, merged with **Create a merge commit**, so `dev` has the fix too

## Rollback

Run the deploy command with the previous version:

```bash
cd /opt/apps/website/docker && sudo ./deploy.sh v1.1.0
```

That puts back that release's image and `compose.yml`. Then fix the problem on a branch and release a new version as usual. Don't delete or move the bad tag.

## Version numbers

`vMAJOR.MINOR.PATCH`, always with the `v`:

| Change | Bump | Example |
|---|---|---|
| Fixes, copy edits | Patch | `v1.2.0` → `v1.2.1` |
| New pages, sections, articles, case studies | Minor | `v1.2.1` → `v1.3.0` |
| A redesign or a big restructure | Major | `v1.3.0` → `v2.0.0` |

`v1.0.0` is the public launch.

## On the server

Run these in `/opt/apps/website/docker`. The folder is root-owned, so everything takes `sudo`.

| To | Run |
|---|---|
| Deploy or roll back | `sudo ./deploy.sh v1.2.0` |
| See which version is live | `sudo grep IMAGE_TAG .env` |
| See what's running | `sudo docker compose ps` |
| Read the logs | `sudo docker compose logs -f web`; the VPS Caddy's: `sudo docker logs caddy-ext-ovhvps1` |
| Apply a `.env` change | Edit it with `sudo nano .env`, then `sudo docker compose up -d` (keeps the same version) |

Copying a new `.env` from your PC replaces the `IMAGE_TAG` line that `deploy.sh` keeps there. After a copy, run `sudo ./deploy.sh <the live version>` instead of `docker compose up -d`.

Don't edit `compose.yml` on the server. Change it in the repo and release, because the next deploy replaces it with the release's copy. The Caddy block for the domain lives in the VPS configuration repo, not here.

## When something goes wrong

| What you see | What to do |
|---|---|
| `git push` is refused: `GH013 ... Changes must be made through a pull request` | The push went to `dev` or `main`, usually because the branch syncs with `dev` (VS Code's **Sync**). Push it under its own name, `git push -u origin <your-branch>`, then open a PR |
| `git branch -d` says the branch `is not fully merged` | Normal after a squash merge. Check that the PR says **Merged** on GitHub, then `git branch -D <name>` |
| The release PR (`dev` → `main`) lists commits that were already released, or shows conflicts | An earlier release PR was squash-merged: [Fix: a squash-merged release PR](#fix-a-squash-merged-release-pr) |
| `docker push` says `denied` or `unauthorized` | `docker login ghcr.io` again, with a token that has `write:packages` |
| A smoke-test line isn't `200` | Don't push. `docker logs site-check` shows the error. Delete the release page on GitHub (the tag stays), then fix it through a PR into `dev`, a new release PR, and a new patch version |
| `./deploy.sh: Permission denied` | Run it as `sudo sh deploy.sh v1.2.0` |
| `manifest unknown` or `pull access denied` | The image isn't pushed, the version is mistyped, or the image is still private (step 6) |
| `network proxy declared as external, but could not be found` | The VPS's Caddy isn't running: `cd /opt/apps/caddy && sudo docker compose up -d` |
| `Your local changes ... would be overwritten by checkout` | Someone edited a file on the server. `sudo git status` shows which. `sudo git checkout -- <file>` throws the edits away (your `.env` is safe: git ignores it). Then deploy again |
| `healthz isn't answering` | `sudo docker compose ps` and `sudo docker compose logs web`. Then the VPS Caddy: `sudo docker logs caddy-ext-ovhvps1`. Common causes: the Caddyfile block isn't live yet (step 10), or DNS doesn't point at the VPS (step 8) |
| The site works but `www` doesn't | Its `A` record is missing or still proxied (orange cloud). It must be DNS only |

## Fix: a squash-merged release PR

When a `dev` → `main` PR is merged with **Squash and merge**, `main` gets one new commit that `dev` doesn't have, even though their files match. The next release PR then lists old commits again and shows conflicts. Fix it once, before that PR, by recording on `dev` that `main` is merged in. No file changes.

First check that `main` holds nothing `dev` lacks (PC, Git Bash):

```bash
git fetch
git log --format='%h %T %s' origin/dev | grep "$(git rev-parse 'origin/main^{tree}')"
```

It should print one line: the `dev` commit whose files are exactly `main`'s. If it prints nothing, stop. `main` has changes `dev` doesn't, and this fix would drop them.

Then:

```bash
git switch dev && git pull
git switch -c fix/merge-main-into-dev
git merge -s ours origin/main -m "chore: merge main into dev after a squashed release"
git diff --stat origin/dev      # prints nothing: no files changed
git push -u origin fix/merge-main-into-dev
```

On GitHub, open a PR with base **`dev`** and compare **`fix/merge-main-into-dev`**. It shows a commit and no file changes; that's expected. Merge it with **Create a merge commit**, not squash: squashing would throw away the link to `main` that this commit exists for. Then **Delete branch**, and on your PC `git switch dev && git pull && git branch -D fix/merge-main-into-dev`. The next release PR shows only the new work.
