#!/usr/bin/env bash
# One-time setup of the Azure staging VM (Ubuntu). Run as azureuser:
#   scp infra/staging/setup-vm.sh azureuser@20.51.113.185: && ssh azureuser@20.51.113.185 'bash setup-vm.sh'
# Afterwards, add the deploy public key it prints to /home/deploy/.ssh/authorized_keys
# (see docs/staging.md) and fill in /opt/django-academy/.env.
set -euo pipefail

APP_DIR=/opt/django-academy

if ! command -v docker >/dev/null; then
  echo "Installing Docker..."
  curl -fsSL https://get.docker.com | sudo sh
fi

if ! id deploy >/dev/null 2>&1; then
  echo "Creating the deploy user (used only by GitHub Actions)..."
  sudo useradd --create-home --shell /bin/bash deploy
fi
sudo usermod -aG docker deploy
sudo mkdir -p /home/deploy/.ssh "$APP_DIR"
sudo touch /home/deploy/.ssh/authorized_keys
sudo chmod 700 /home/deploy/.ssh && sudo chmod 600 /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh "$APP_DIR"

# Nightly database dump, kept for 14 days.
sudo tee /etc/cron.d/django-academy-backup >/dev/null <<'CRON'
15 3 * * * deploy cd /opt/django-academy && mkdir -p backups && docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > backups/chips-$(date +\%F).sql.gz && find backups -name '*.sql.gz' -mtime +14 -delete
30 3 * * * deploy cd /opt/django-academy && mkdir -p backups && docker compose run --rm --no-deps -T api tar czf - -C /app media > backups/media-$(date +\%F).tgz && find backups -name 'media-*.tgz' -mtime +14 -delete
CRON

echo
echo "Done. Next steps:"
echo "  1. Azure portal > VM > Networking: allow inbound TCP 80 and 8080."
echo "  2. DNS: A record staging.hbcuchip.org -> this VM's public IP."
echo "  3. Put the GitHub Actions deploy public key in /home/deploy/.ssh/authorized_keys."
echo "  4. Copy infra/staging/{compose.yml,Caddyfile,deploy.sh} to $APP_DIR and create $APP_DIR/.env."
