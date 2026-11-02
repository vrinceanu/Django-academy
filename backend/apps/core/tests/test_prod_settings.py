"""The production storage guard, checked in a fresh interpreter per case."""

import os
import subprocess
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[3]


def load_prod_settings(**overrides: str) -> subprocess.CompletedProcess[str]:
    env = {
        **{k: v for k, v in os.environ.items() if k != "ENVIRONMENT"},
        "DJANGO_SETTINGS_MODULE": "config.settings.prod",
        "DJANGO_SECRET_KEY": "x" * 50,
        "S3_ENDPOINT_URL": "",
        **overrides,
    }
    code = "import django; django.setup()"
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=BACKEND,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_production_refuses_local_disk():
    result = load_prod_settings()  # ENVIRONMENT unset means production
    assert result.returncode != 0
    assert "Production needs S3_ENDPOINT_URL" in result.stderr


def test_staging_may_use_local_disk():
    result = load_prod_settings(ENVIRONMENT="staging")
    assert result.returncode == 0, result.stderr


def test_production_with_r2_starts():
    result = load_prod_settings(
        ENVIRONMENT="production", S3_ENDPOINT_URL="https://example.r2.cloudflarestorage.com"
    )
    assert result.returncode == 0, result.stderr
