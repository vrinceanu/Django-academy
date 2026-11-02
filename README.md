# django-academy — CHIPS Academy

The learning platform for the HBCU CHIPS Network: cohort-based microcredentials in
semiconductors and microelectronics, with verifiable badges and certificates.

The repository is named `django-academy`. Python packages inside keep their design names
(`config`, `apps.*`) so nothing shadows the Django framework itself (see
`docs/adr/0001-project-name.md`).

| Folder | What it holds |
| --- | --- |
| `backend/` | Django + DRF API, Celery tasks (`config/`, `apps/`) |
| `frontend/` | Next.js app: public pages, `/learn`, `/teach`, `/studio`, `/manage`, `/account` |
| `content/` | Sample and pilot content packages (schema 1) |
| `docs/` | ADRs and runbooks |
| `infra/staging/` | Azure VM stack, Caddy, setup and deploy scripts |

Design documents live one level up, in the LMS folder (concept, Django design,
Phase 1 build plan).

## Run it locally

You need Docker with Compose v2: Docker Desktop, or Colima with the Homebrew
`docker-compose` package. Commands below use `docker compose`; with the standalone
package type `docker-compose` instead (the Makefile picks whichever you have).

```sh
cp .env.example .env
docker compose up --build
```

With Colima, give it enough room for the stack: `colima start --cpu 4 --memory 6`.
Uploaded files are stored in `backend/media/`. Staging keeps them on the VM's disk
until M3; production uses Cloudflare R2.

| Service | Address |
| --- | --- |
| Web | http://localhost:3000 |
| API | http://localhost:8000/api/v1/health/ |
| API docs | http://localhost:8000/api/v1/docs/ (sign in to /ops/admin/ first) |
| Operations admin | http://localhost:8000/ops/admin/ |

Create an admin for `/ops/admin/`:

```sh
docker compose exec api python manage.py createsuperuser
```

## Everyday commands

```sh
make test        # backend tests with coverage
make lint        # ruff, mypy, eslint, tsc
make schema      # regenerate openapi.yaml and the typed frontend client
make migrations  # makemigrations after model changes
```

CI runs all of these on every pull request, then starts the full compose stack.
A green build of `main` deploys to staging at https://staging.hbcuchip.org:8080
(see `docs/staging.md`).

## Rules every app follows

- Other apps call an app only through its `services.py`, or listen to its signals.
- Every staff write calls `audit.record()` in the same transaction.
- Every object permission is a rule in `apps/core/permissions.py`.
- All author markdown is rendered with `apps.core.markdown.render_markdown`.
- API routes are grouped by caller in `config/urls.py`, never by app.
