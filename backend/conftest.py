import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(django_user_model):  # type: ignore[no-untyped-def]
    return django_user_model.objects.create_user(email="Student@HBCUchips.org", first_name="Ada")


@pytest.fixture
def staff(django_user_model):  # type: ignore[no-untyped-def]
    return django_user_model.objects.create_user(email="admin@hbcuchips.org", is_staff=True)
