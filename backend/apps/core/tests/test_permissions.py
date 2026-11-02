import pytest
from django.contrib.auth.models import AnonymousUser

from apps.core.permissions import UnknownPermission, can, registered_rules, rule


@pytest.mark.django_db
def test_anonymous_can_do_nothing():
    assert can(AnonymousUser(), "ops.view_admin") is False
    assert can(None, "ops.view_admin") is False


@pytest.mark.django_db
def test_staff_rule(user, staff):
    assert can(staff, "ops.view_admin") is True
    assert can(user, "ops.view_admin") is False


@pytest.mark.django_db
def test_inactive_user_denied(staff):
    staff.is_active = False
    assert can(staff, "ops.view_admin") is False


@pytest.mark.django_db
def test_unknown_action_raises(user):
    with pytest.raises(UnknownPermission):
        can(user, "nope.nothing")


@pytest.mark.django_db
def test_superuser_allowed_everything(django_user_model):
    root = django_user_model.objects.create_superuser(email="root@hbcuchips.org")
    assert can(root, "anything.at_all") is True


def test_duplicate_rule_rejected():
    assert "ops.view_admin" in registered_rules()
    with pytest.raises(ValueError):
        rule("ops.view_admin")(lambda u, o: True)
