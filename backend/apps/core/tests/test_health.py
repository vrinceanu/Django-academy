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
