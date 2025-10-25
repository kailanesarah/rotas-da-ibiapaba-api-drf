from rest_framework import serializers
from accounts.models.user import User


class AdminUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar usuários do tipo 'admin'.
    """

    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_superuser(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type="admin",
        )
