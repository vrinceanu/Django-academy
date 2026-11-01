from django.db import connection
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    """Liveness and database check for Caddy, Docker and uptime monitors."""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    @extend_schema(
        responses=inline_serializer(
            "Health", {"status": serializers.CharField(), "database": serializers.CharField()}
        )
    )
    def get(self, request: Request) -> Response:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db = "ok"
        except Exception:
            db = "unavailable"
        status = "ok" if db == "ok" else "degraded"
        return Response({"status": status, "database": db}, status=200 if db == "ok" else 503)
