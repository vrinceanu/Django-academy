from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.health import check


# HealthCheckMiddleware normally answers first; this view documents the endpoint in
# the API schema and serves it if the middleware is ever removed.
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
        body, status = check()
        return Response(body, status=status)
