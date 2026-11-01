"""Every object-level permission in the project lives here (design rule).

Apps register rules with ``@rule("<app>.<action>")``; views and services ask
``can(user, "<app>.<action>", obj)``. Keeping rules in one module makes them
easy to review and to test as a role x object table.

M0 ships the registry and the staff/anonymous basics. Role rules (student,
instructor, reviewer, author, admin) arrive with ``accounts`` roles in M1.
"""

from collections.abc import Callable
from typing import Any

from rest_framework.permissions import BasePermission

Rule = Callable[[Any, Any], bool]
_RULES: dict[str, Rule] = {}


class UnknownPermission(LookupError):
    pass


def rule(name: str) -> Callable[[Rule], Rule]:
    def register(fn: Rule) -> Rule:
        if name in _RULES:
            raise ValueError(f"Permission rule already registered: {name}")
        _RULES[name] = fn
        return fn

    return register


def can(user: Any, action: str, obj: Any = None) -> bool:
    """Return True if ``user`` may perform ``action`` (on ``obj``, if given)."""
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if not getattr(user, "is_active", False):
        return False
    if getattr(user, "is_superuser", False):
        return True
    try:
        check = _RULES[action]
    except KeyError as exc:
        raise UnknownPermission(action) from exc
    return bool(check(user, obj))


def registered_rules() -> list[str]:
    return sorted(_RULES)


@rule("ops.view_admin")
def _ops_view_admin(user: Any, obj: Any) -> bool:
    return bool(user.is_staff)


class Can(BasePermission):
    """DRF permission backed by ``can()``.

    ``Can.to("manage.view_people")`` checks once per request (no object).
    ``Can.to("catalog.edit", per_object=True)`` checks each object the view loads.
    """

    action: str = ""
    per_object: bool = False

    @classmethod
    def to(cls, action: str, per_object: bool = False) -> type["Can"]:
        name = f"Can_{action.replace('.', '_')}"
        return type(name, (cls,), {"action": action, "per_object": per_object})

    def has_permission(self, request, view) -> bool:  # type: ignore[no-untyped-def]
        if self.per_object:
            user = request.user
            return bool(user and user.is_authenticated and user.is_active)
        return can(request.user, self.action)

    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore[no-untyped-def]
        return can(request.user, self.action, obj) if self.per_object else True
