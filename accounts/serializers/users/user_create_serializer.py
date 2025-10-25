from rest_framework import serializers
from accounts.models.user import User


class EstablishmentUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            type="establishment",
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
