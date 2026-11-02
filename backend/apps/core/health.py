"""Health check shared by the API view and the middleware below."""

from collections.abc import Callable

from django.db import connection
from django.http import HttpRequest, HttpResponse, JsonResponse

HEALTH_PATH = "/api/v1/health/"


def check() -> tuple[dict[str, str], int]:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db = "ok"
    except Exception:
        db = "unavailable"
    ok = db == "ok"
    return {"status": "ok" if ok else "degraded", "database": db}, 200 if ok else 503


class HealthCheckMiddleware:
    """Answer GET /api/v1/health/ before host validation.

    Docker and the deploy script probe the API inside the container as
    ``localhost:8000``, which is not (and should not be) in ALLOWED_HOSTS. The
    answer reveals nothing but up/down, so it is safe for any Host header.
    Must be first in MIDDLEWARE.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method in ("GET", "HEAD") and request.path == HEALTH_PATH:
            body, status = check()
            return JsonResponse(body, status=status)
        return self.get_response(request)
