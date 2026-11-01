"""The only entry point other apps use: ``audit.record(...)``.

Call it inside the same transaction as the write it describes, so the event and
the change commit or roll back together (ATOMIC_REQUESTS covers API views).
"""

from typing import Any

from django.db import models

from .models import AuditEvent


def _client_ip(request: Any) -> str | None:
    if request is None:
        return None
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip() or None
    return request.META.get("REMOTE_ADDR") or None


def record(
    action: str,
    *,
    actor: Any = None,
    target: models.Model | None = None,
    data: dict[str, Any] | None = None,
    request: Any = None,
    actor_label: str | None = None,
) -> AuditEvent:
    """Write one audit event.

    ``actor`` defaults to ``request.user``; pass ``actor_label`` (e.g. a job name)
    for system actions with no user.
    """
    if actor is None and request is not None and request.user.is_authenticated:
        actor = request.user
    if actor is not None and not getattr(actor, "is_authenticated", True):
        actor = None
    label = actor_label or (getattr(actor, "email", "") if actor else "") or "system"
    return AuditEvent.objects.create(
        actor=actor,
        actor_label=label,
        action=action,
        target_type=target._meta.label_lower if target is not None else "",
        target_id=str(target.pk) if target is not None else "",
        target_label=str(target)[:255] if target is not None else "",
        data=data or {},
        ip_address=_client_ip(request),
    )
