#!/usr/bin/env bash
# Runs on the VM (as deploy) for every merge to main. Usage: deploy.sh <image-tag>
set -euo pipefail
cd /opt/django-academy

TAG="${1:?usage: deploy.sh <image-tag>}"
sed -i "s/^IMAGE_TAG=.*/IMAGE_TAG=${TAG}/" .env

docker compose pull api web
docker compose up -d postgres redis
docker compose run --rm api python manage.py migrate --noinput
docker compose run --rm api python manage.py ensure_buckets
docker compose up -d --remove-orphans
docker image prune -f >/dev/null

# Fail the deploy if the site is not healthy within a minute.
for _ in $(seq 1 30); do
  if docker compose exec -T api curl -fsS http://localhost:8000/api/v1/health/ >/dev/null; then
    echo "Deployed ${TAG}."
    exit 0
  fi
  sleep 2
done
echo "Health check failed after deploying ${TAG}." >&2
docker compose logs --tail=50 api >&2
exit 1
