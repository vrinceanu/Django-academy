"""Test runs (pytest, CI). Postgres is required; everything else is in-process."""

from .base import *

SECRET_KEY = "test-secret-key"  # noqa: S105
DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
STORAGES = {
    **STORAGES,
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "public": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
MIDDLEWARE = [m for m in MIDDLEWARE if "whitenoise" not in m]
