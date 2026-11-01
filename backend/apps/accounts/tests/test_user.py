import pytest


@pytest.mark.django_db
def test_email_is_login_and_normalized(user):
    assert user.email == "student@hbcuchip.org"
    assert user.has_usable_password() is False  # Google sign-in, no local password


@pytest.mark.django_db
def test_email_lookup_ignores_case(django_user_model, user):
    assert django_user_model.objects.get_by_natural_key("STUDENT@hbcuchip.org") == user


@pytest.mark.django_db
def test_display_name(user):
    user.last_name = "Lovelace"
    assert user.display_name == "Ada Lovelace"
    user.preferred_name = "Addie"
    assert user.display_name == "Addie Lovelace"


@pytest.mark.django_db
def test_superuser(django_user_model):
    root = django_user_model.objects.create_superuser(email="root@hbcuchip.org", password="x")
    assert root.is_staff and root.is_superuser and root.check_password("x")


@pytest.mark.django_db
def test_me_requires_login(api_client):
    assert api_client.get("/api/v1/me/").status_code == 403


@pytest.mark.django_db
def test_me_returns_current_user(api_client, user):
    api_client.force_authenticate(user)
    body = api_client.get("/api/v1/me/").json()
    assert body["email"] == "student@hbcuchip.org"
    assert body["display_name"] == "Ada"
