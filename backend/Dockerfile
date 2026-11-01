# CHIPS Academy backend: Django API, Celery worker and beat share this image.
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ffmpeg is added to the worker image in M3 (media pipeline).
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq5 curl \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 1000 app

WORKDIR /app
COPY pyproject.toml ./
RUN mkdir -p config apps && pip install .  # dependency layer, cached until pyproject changes

COPY . .
RUN pip install --no-deps -e .

FROM base AS dev
RUN pip install -e ".[dev]"
USER app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS prod
ENV DJANGO_SETTINGS_MODULE=config.settings.prod
RUN DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD curl -fsS http://localhost:8000/api/v1/health/ || exit 1
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "--access-logfile", "-"]
