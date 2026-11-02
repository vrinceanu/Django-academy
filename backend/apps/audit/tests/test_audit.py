import pytest
from django.test import RequestFactory

from apps.audit import services as audit
from apps.audit.models import AppendOnlyError, AuditEvent


@pytest.mark.django_db
def test_record_with_actor_and_target(staff, user):
    event = audit.record("people.update", actor=staff, target=user, data={"field": "first_name"})
    assert event.actor == staff
    assert event.actor_label == "admin@hbcuchips.org"
    assert event.target_type == "accounts.user"
    assert event.target_id == str(user.pk)
    assert event.data == {"field": "first_name"}


@pytest.mark.django_db
def test_record_from_request_uses_user_and_ip(staff):
    request = RequestFactory().post("/x", HTTP_X_FORWARDED_FOR="203.0.113.7, 10.0.0.1")
    request.user = staff
    event = audit.record("cycles.create", request=request)
    assert event.actor == staff
    assert event.ip_address == "203.0.113.7"


@pytest.mark.django_db
def test_system_event_has_label():
    event = audit.record("retention.apply", actor_label="job:apply_retention")
    assert event.actor is None
    assert event.actor_label == "job:apply_retention"


@pytest.mark.django_db
def test_events_are_append_only(staff):
    event = audit.record("people.import", actor=staff)
    event.action = "changed"
    with pytest.raises(AppendOnlyError):
        event.save()
    with pytest.raises(AppendOnlyError):
        event.delete()
    with pytest.raises(AppendOnlyError):
        AuditEvent.objects.all().update(action="x")
    with pytest.raises(AppendOnlyError):
        AuditEvent.objects.all().delete()
