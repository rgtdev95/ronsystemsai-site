#!/bin/sh
# Put a release on the server, or roll back to an older one. Same command either way:
#   cd ~/ronsystemsai/docker && ./deploy.sh v1.2.0
# Versions are on the repo's GitHub Releases page.
#
# ~/ronsystemsai is a clone of the repo. The script checks out the release's tag (so this
# compose.yml and Caddyfile match the release), records the version as IMAGE_TAG in .env,
# starts that release's image and waits until it's healthy.
set -eu

SITE=https://ronsystemsai.com

main() {
  version="${1:-}"
  case "$version" in
    v[0-9]*.[0-9]*.[0-9]*) ;;
    *) echo "Usage: ./deploy.sh v1.2.0   (a version from the GitHub Releases page)" >&2; exit 2 ;;
  esac

  cd "$(dirname "$0")"
  if [ ! -f .env ]; then
    echo "No .env next to compose.yml. Copy your .env here first (see .env.example)." >&2
    exit 1
  fi

  echo "==> Getting $version from GitHub"
  git fetch --quiet --tags --force origin
  git -c advice.detachedHead=false checkout --quiet "refs/tags/$version"

  echo "==> Recording IMAGE_TAG=$version in .env"
  if grep -q '^IMAGE_TAG=' .env; then
    sed -i "s/^IMAGE_TAG=.*/IMAGE_TAG=$version/" .env
  else
    printf '\n# Set by deploy.sh: the release running on this server.\nIMAGE_TAG=%s\n' "$version" >> .env
  fi

  echo "==> Starting $version"
  docker compose pull --quiet web
  docker compose up -d --remove-orphans --wait
  docker image prune -f > /dev/null

  if ! curl -fsS -o /dev/null --retry 10 --retry-delay 3 --retry-all-errors "$SITE/healthz"; then
    echo "The containers are up, but $SITE/healthz isn't answering. Check: docker compose logs caddy web" >&2
    exit 1
  fi
  echo "==> Live: $version at $SITE"

  ping_indexnow
}

# Ask Bing and other IndexNow engines to recrawl every page in the sitemap. Optional:
# only when INDEXNOW_KEY is set in .env, and a failure here doesn't fail the deploy.
ping_indexnow() {
  key=$(sed -n 's/^INDEXNOW_KEY=//p' .env | tr -d '"\r')
  [ -n "$key" ] || return 0
  urls=$(curl -fsS "$SITE/sitemap.xml" | grep -o '<loc>[^<]*' | sed 's/<loc>/"/; s/$/"/' | paste -sd, -)
  if [ -n "$urls" ] && curl -fsS -o /dev/null -H 'Content-Type: application/json; charset=utf-8' \
      -d "{\"host\":\"${SITE#https://}\",\"key\":\"$key\",\"urlList\":[$urls]}" \
      https://api.indexnow.org/indexnow; then
    echo "==> Asked search engines to recrawl (IndexNow)"
  else
    echo "    IndexNow ping failed (optional, the site is fine)"
  fi
}

# Everything is in functions and runs from this one line, so the shell has read the whole
# script before `git checkout` replaces this file with the release's copy.
main "$@"; exit
