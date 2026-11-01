"""Custom user, created in the first migration so nothing has to be rewritten later.

M0 keeps it minimal: the Network email is the login, there is no username, and
the primary key is a UUID. M1 adds roles, Google sign-in (allauth), MFA for
staff, school membership and the welcome/consent flow.
"""

import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager["User"]):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra: object) -> "User":
        if not email:
            raise ValueError("An email address is required.")
        user = self.model(email=self.normalize_email(email).lower(), **extra)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # Network accounts sign in with Google
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra: object) -> "User":
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email: str, password: str | None = None, **extra: object) -> "User":
        extra["is_staff"] = True
        extra["is_superuser"] = True
        return self._create_user(email, password, **extra)

    def get_by_natural_key(self, username: str | None) -> "User":
        return self.get(email__iexact=username)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("Network email", unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    preferred_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(
        default=False, help_text="Can open the operations admin at /ops/admin/."
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["last_name", "first_name", "email"]

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    @property
    def display_name(self) -> str:
        first = self.preferred_name or self.first_name
        full = f"{first} {self.last_name}".strip()
        return full or self.email
