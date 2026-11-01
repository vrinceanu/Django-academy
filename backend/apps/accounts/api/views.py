from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MeSerializer


class MeView(APIView):
    """The signed-in user. Profile editing and consents arrive in M1."""

    @extend_schema(responses=MeSerializer)
    def get(self, request: Request) -> Response:
        return Response(MeSerializer(request.user).data)
