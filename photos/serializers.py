from rest_framework import serializers
from photos.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Photo
        fields = ['id', 'establishment', 'image', 'alt_text',
                  'is_profile_pic', 'is_gallery_pic', 'is_product_pic']
        read_only_fields = ['id']
