# Staging on the Azure VM

Staging and demos run at **https://staging.hbcuchip.org:8080** on the Azure VM
(`20.51.113.185`). Each green build of `main` deploys there automatically.

## One-time setup

1. **Network.** In the Azure portal, open the VM's networking rules and allow inbound
   TCP **80** (Let's Encrypt certificate challenge) and **8080** (the site).
2. **DNS.** Point an A record for `staging.hbcuchip.org` at `20.51.113.185`.
3. **Prepare the VM.** From your Mac, using your own key (keep it out of the repo):

   ```sh
   scp -i <your-key.pem> infra/staging/setup-vm.sh azureuser@20.51.113.185:
   ssh -i <your-key.pem> azureuser@20.51.113.185 'bash setup-vm.sh'
   ```

   This installs Docker, creates a `deploy` user for GitHub Actions and schedules a
   nightly database dump.
4. **Deploy key.** Make a key used only by GitHub Actions:

   ```sh
   ssh-keygen -t ed25519 -f staging_deploy -C "github-actions-staging" -N ""
   ```

   Append `staging_deploy.pub` to `/home/deploy/.ssh/authorized_keys` on the VM.
5. **Environment file.** On the VM, copy `infra/staging/.env.example` to
   `/opt/django/.env` (owned by `deploy`) and fill in every value. Generate secrets
   with `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`.
6. **GitHub secrets** (repo Settings, Secrets and variables, Actions, environment
   `staging`):

   | Secret | Value |
   | --- | --- |
   | `STAGING_SSH_KEY` | contents of `staging_deploy` (the private key) |
   | `STAGING_HOST` | `20.51.113.185` |
   | `GHCR_READ_TOKEN` | a fine-grained token with `read:packages`, so the VM can pull images |

7. Run the **Deploy staging** workflow once by hand (Actions tab), then open the site.

## Day to day

- Logs: `ssh deploy@20.51.113.185 'cd /opt/django && docker compose logs -f api'`
- Admin user: `docker compose exec api python manage.py createsuperuser`
- Backups: `/opt/django/backups/`, one gzip dump per night, 14 days kept.
