from rest_framework import serializers
from accounts.models.location import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "country",
            "state",
            "city",
            "CEP",
            "neighborhood",
            "street",
            "number",
            "complement",
        ]
