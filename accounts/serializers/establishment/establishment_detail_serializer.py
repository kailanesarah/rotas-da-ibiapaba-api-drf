from rest_framework import serializers
from accounts.models.establishment import Establishment
from accounts.serializers.base.location_serializer import LocationSerializer
from accounts.serializers.base.social_media_serializer import SocialMediaSerializer
from accounts.serializers.base.user_info_serializer import (
    EstablishmentUserInfoSerializer,
)
from categories.serializers import CategorySerializer
from photos.utils import PhotoUtils


class EstablishmentDetailSerializer(serializers.ModelSerializer):
    user = EstablishmentUserInfoSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    social_media = SocialMediaSerializer(read_only=True)
    categories = CategorySerializer(source="category", many=True, read_only=True)

    profile_photo = serializers.SerializerMethodField()
    gallery_photos = serializers.SerializerMethodField()
    product_photos = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = [
            "id",
            "user",
            "name",
            "description",
            "cnpj",
            "social_media",
            "location",
            "categories",
            "pix_key",
            "profile_photo",
            "gallery_photos",
            "product_photos",
        ]

    def get_profile_photo(self, obj):
        return PhotoUtils.get_photo_url_by_type(obj.photos, "profile")

    def get_gallery_photos(self, obj):
        return PhotoUtils.get_multiple_photo_urls_by_types(obj.photos, ["gallery"])

    def get_product_photos(self, obj):
        return PhotoUtils.get_multiple_photo_urls_by_types(obj.photos, ["product"])
