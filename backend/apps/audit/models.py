"""Append-only audit log. Every staff write records one event (design rule)."""

from django.conf import settings
from django.db import models

from apps.core.models import UUIDModel


class AppendOnlyError(Exception):
    pass


class AuditEventQuerySet(models.QuerySet):
    def update(self, **kwargs):  # type: ignore[no-untyped-def]
        raise AppendOnlyError("Audit events cannot be updated.")

    def delete(self):  # type: ignore[no-untyped-def]
        raise AppendOnlyError("Audit events cannot be deleted.")


class AuditEvent(UUIDModel):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_events",
        help_text="Empty for system jobs (Celery, management commands).",
    )
    actor_label = models.CharField(
        max_length=254, help_text="Email or job name, kept if the user is later removed."
    )
    action = models.CharField(max_length=100, db_index=True, help_text="e.g. people.import")
    target_type = models.CharField(max_length=100, blank=True, db_index=True)
    target_id = models.CharField(max_length=64, blank=True, db_index=True)
    target_label = models.CharField(max_length=255, blank=True)
    data = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    objects = AuditEventQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["target_type", "target_id", "-created_at"])]

    def __str__(self) -> str:
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.actor_label} {self.action}"

    def save(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        if not self._state.adding:
            raise AppendOnlyError("Audit events cannot be changed once written.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise AppendOnlyError("Audit events cannot be deleted.")
