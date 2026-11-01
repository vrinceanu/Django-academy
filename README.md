# django — CHIPS Academy

The learning platform for the HBCU CHIPS Network: cohort-based microcredentials in
semiconductors and microelectronics, with verifiable badges and certificates.

The repository is named `django`; Python packages inside keep their design names
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

You need Docker Desktop.

```sh
cp .env.example .env
docker compose up --build
```

| Service | Address |
| --- | --- |
| Web | http://localhost:3000 |
| API | http://localhost:8000/api/v1/health/ |
| API docs | http://localhost:8000/api/v1/docs/ (sign in to /ops/admin/ first) |
| Operations admin | http://localhost:8000/ops/admin/ |
| MinIO console | http://localhost:9001 (minio / minio-secret) |

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
