from rest_framework import serializers
from accounts.models.establishment import Establishment
from accounts.models.user import User
from accounts.models.location import Location
from accounts.models.social_media import SocialMedia
from categories.models import Category
from categories.serializers import CategorySerializer
from accounts.serializers.base.user_info_serializer import (
    EstablishmentUserInfoSerializer,
)
from accounts.serializers.base.location_serializer import LocationSerializer
from accounts.serializers.base.social_media_serializer import SocialMediaSerializer
from accounts.serializers.users.user_create_serializer import (
    EstablishmentUserCreateSerializer,
)
from accounts.utils.username_utils import UniqueUsernameGenerator, UsernameUtils
from photos.utils import PhotoUtils


class EstablishmentCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.DictField(write_only=True)
    user_info = EstablishmentUserInfoSerializer(source="user", read_only=True)

    location = LocationSerializer()
    social_media = SocialMediaSerializer(required=False)

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, write_only=True
    )
    categories = CategorySerializer(many=True, read_only=True, source="category")

    profile_photo = serializers.SerializerMethodField()
    gallery_photos = serializers.SerializerMethodField()
    product_photos = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = [
            "id",
            "user",
            "user_info",
            "name",
            "description",
            "cnpj",
            "social_media",
            "location",
            "category",
            "categories",
            "pix_key",
            "profile_photo",
            "gallery_photos",
            "product_photos",
        ]

    # --- Métodos auxiliares de imagem ---
    def get_profile_photo(self, obj):
        return PhotoUtils.get_photo_url_by_type(obj.photos, "profile")

    def get_gallery_photos(self, obj):
        return PhotoUtils.get_multiple_photo_urls_by_types(obj.photos, ["gallery"])

    def get_product_photos(self, obj):
        return PhotoUtils.get_multiple_photo_urls_by_types(obj.photos, ["product"])

    # --- Métodos principais ---
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        location_data = validated_data.pop("location")
        social_media_data = validated_data.pop("social_media", None)
        category_ids = validated_data.pop("category")

        base_name = validated_data.get("name", "estabelecimento")
        user_data["username"] = UniqueUsernameGenerator().generate_unique_username(
            base_name
        )

        email = user_data.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Este e-mail já está em uso."})

        user_serializer = EstablishmentUserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        location = Location.objects.create(**location_data)
        social_media = (
            SocialMedia.objects.create(**social_media_data)
            if social_media_data
            else None
        )

        establishment = Establishment.objects.create(
            user=user, location=location, social_media=social_media, **validated_data
        )

        establishment.category.set(category_ids)
        return establishment

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        location_data = validated_data.pop("location", None)
        social_media_data = validated_data.pop("social_media", None)
        category_ids = validated_data.pop("category", None)

        old_username = instance.user.username

        # Atualiza usuário
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == "password":
                    user.set_password(value)
                elif attr == "username":
                    setattr(user, attr, value)
                    UsernameUtils().update_rename_folder(instance, old_username, value)
                else:
                    setattr(user, attr, value)
            user.save()

        # Atualiza localização
        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()

        # Atualiza redes sociais
        if social_media_data:
            if instance.social_media:
                for attr, value in social_media_data.items():
                    setattr(instance.social_media, attr, value)
                instance.social_media.save()
            else:
                instance.social_media = SocialMedia.objects.create(**social_media_data)

        # Atualiza categorias
        if category_ids is not None:
            instance.category.set(category_ids)

        # Atualiza dados gerais
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
