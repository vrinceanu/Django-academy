from rest_framework import serializers

from ..models import User


class MeSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "preferred_name",
            "display_name",
            "is_staff",
        ]
        read_only_fields = fields
