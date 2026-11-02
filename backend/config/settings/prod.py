"""Staging and production. Every secret comes from the environment."""

import sentry_sdk

from .base import *

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")  # required, no default
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "CHIPS Academy <no-reply@hbcuchips.org>")

# TLS ends at Caddy, which forwards over the internal Docker network.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(env("SECURE_HSTS_SECONDS", "0"))  # raise once HTTPS is proven
SECURE_CONTENT_TYPE_NOSNIFF = True

# "production" unless the environment says otherwise, so the guard below fails safe.
ENVIRONMENT = env("ENVIRONMENT", "production")

# Production must keep files in Cloudflare R2. Staging may use the VM's disk (a Docker
# volume at MEDIA_ROOT) until the media pipeline arrives in M3.
if ENVIRONMENT == "production" and not USE_S3:
    raise RuntimeError("Production needs S3_ENDPOINT_URL (Cloudflare R2).")

if dsn := env("SENTRY_DSN", ""):
    sentry_sdk.init(
        dsn=dsn, environment=ENVIRONMENT, traces_sample_rate=0.05, send_default_pii=False
    )
