from rest_framework import serializers
from accounts.models.user import User


class EstablishmentUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username"]
