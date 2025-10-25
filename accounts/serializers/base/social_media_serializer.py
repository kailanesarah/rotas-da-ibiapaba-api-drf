from rest_framework import serializers
from accounts.models.social_media import SocialMedia


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = [
            "whatsapp",
            "instagram",
            "facebook",
        ]
