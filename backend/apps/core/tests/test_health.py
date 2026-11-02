import pytest


@pytest.mark.django_db
def test_health_ok(api_client):
    response = api_client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


@pytest.mark.django_db
def test_schema_is_published(api_client, staff):
    api_client.force_authenticate(staff)
    response = api_client.get("/api/v1/schema/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_health_answers_for_any_host(client, settings):
    """Docker and deploy.sh probe as localhost:8000, which is not an allowed host."""
    settings.ALLOWED_HOSTS = ["staging.hbcuchips.org"]
    response = client.get("/api/v1/health/", HTTP_HOST="localhost:8000")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.django_db
def test_other_paths_still_validate_host(client, settings):
    settings.ALLOWED_HOSTS = ["staging.hbcuchips.org"]
    response = client.get("/api/v1/me/", HTTP_HOST="localhost:8000")
    assert response.status_code == 400


@pytest.mark.django_db
def test_health_reports_database_outage(client, monkeypatch):
    from apps.core import health

    def broken_cursor():
        raise RuntimeError("database down")

    monkeypatch.setattr(health.connection, "cursor", broken_cursor)
    response = client.get("/api/v1/health/")
    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "unavailable"}
