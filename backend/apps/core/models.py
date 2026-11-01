"""Abstract base models every app builds on."""

import uuid

from django.db import models


class UUIDModel(models.Model):
    """UUID primary key, so ids in URLs never reveal counts or order."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel):
    """Default base for project models: UUID key plus timestamps."""

    class Meta:
        abstract = True
