from rest_framework import serializers
from photos.models import EstablishmentProfileImage


class EstablishmentProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstablishmentProfileImage
        fields = [
            'id',
            'image',
            'image_url',
            'alt_text',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
