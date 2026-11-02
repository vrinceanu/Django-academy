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
5. **Files.** Staging keeps uploaded files on the VM's disk (Docker volume
   `media_data`) until M3. Nothing to set up now; see "Moving to Cloudflare R2" below.
6. **Environment file.** On the VM, copy `infra/staging/.env.example` to
   `/opt/django-academy/.env` (owned by `deploy`) and fill in every value. Generate secrets
   with `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`.
7. **GitHub secrets.** On the repo: Settings, Secrets and variables, Actions,
   New repository secret.

   | Secret | Value |
   | --- | --- |
   | `STAGING_SSH_KEY` | contents of `staging_deploy` (the private key, including the BEGIN/END lines) |
   | `STAGING_HOST` | `20.51.113.185` |
   | `GHCR_READ_TOKEN` | a personal access token (classic) with only `read:packages`, so the VM can pull images |

   The container registry does not accept fine-grained tokens. Create the classic token at
   https://github.com/settings/tokens/new?scopes=read:packages and give it an expiry you
   will remember: when it lapses, deploys fail at the image pull until it is replaced.
   The token lives only in GitHub secrets; the deploy job hands it to the VM for each pull.

8. Run the **Deploy staging** workflow once by hand (Actions tab), then open the site.

## Day to day

- Logs: `ssh deploy@20.51.113.185 'cd /opt/django-academy && docker compose logs -f api'`
- Admin user: `docker compose exec api python manage.py createsuperuser`
- Backups: `/opt/django-academy/backups/`, a database dump and a media archive per
  night, 14 days kept.

## Moving to Cloudflare R2 (M3)

Before lecture video arrives, staging moves its files to R2, as production will:

1. In the Cloudflare dashboard, create two R2 buckets, `chips-staging-private` and
   `chips-staging-public`, and an R2 API token with Object Read & Write on those two
   buckets only. Note the account ID for the endpoint.
2. Fill in the `S3_*` lines in `/opt/django-academy/.env` and redeploy.

Production has no disk fallback: it refuses to start without `S3_ENDPOINT_URL`.
