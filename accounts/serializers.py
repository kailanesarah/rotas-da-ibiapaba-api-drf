from rest_framework import serializers
from accounts.models import Location, Establishment, User, SocialMedia
from categories.models import Category
from photos.models import Photo
from categories.serializers import CategorySerializer
from photos.serializers import PhotoSerializer


class AdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            type='admin'
        )
        return user


class EstablishmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            type='establishment',
            is_staff=False,
            is_superuser=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Photo
        fields = ['id', 'image', 'alt_text']
        read_only_fields = ['id']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'


class EstablishmentSerializer(serializers.ModelSerializer):
    user = EstablishmentCreateSerializer()
    location = LocationSerializer()
    social_media = SocialMediaSerializer()

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    categories = CategorySerializer(
        many=True, read_only=True, source='category'
    )

    profile_photo = serializers.SerializerMethodField()
    gallery_photos = serializers.SerializerMethodField()
    product_photos = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = [
            'id', 'user', 'name', 'description', 'cnpj',
            'social_media', 'location', 'category', 'categories', 'pix_key',
            'profile_photo', 'gallery_photos', 'product_photos'
        ]

    def get_profile_photo(self, obj):
        profile_photo_instance = obj.get_profile_photo()
        if profile_photo_instance:
            return PhotoSerializer(profile_photo_instance, context=self.context).data
        return None

    def get_gallery_photos(self, obj):
        gallery_photos_qs = obj.get_gallery_photos()
        if gallery_photos_qs:
            return PhotoSerializer(gallery_photos_qs, many=True, context=self.context).data
        return None

    def get_product_photos(self, obj):
        product_photos_qs = obj.get_product_photos()
        if product_photos_qs:
            return PhotoSerializer(product_photos_qs, many=True, context=self.context).data
        return None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        location_data = validated_data.pop('location')
        social_media_data = validated_data.pop('social_media', None)
        category_ids = validated_data.pop('category')

        user = EstablishmentCreateSerializer().create(validated_data=user_data)
        location = Location.objects.create(**location_data)

        social_media = None
        if social_media_data:
            social_media = SocialMedia.objects.create(**social_media_data)

        establishment = Establishment.objects.create(
            user=user,
            location=location,
            social_media=social_media,
            **validated_data
        )

        establishment.category.set(category_ids)

        return establishment
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        location_data = validated_data.pop('location', None)
        social_media_data = validated_data.pop('social_media', None)
        category_ids = validated_data.pop('category', None)

        # Atualiza os campos simples do Establishment
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Atualiza o User aninhado
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == 'password':
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()

        # Atualiza a Location aninhada
        if location_data:
            location = instance.location
            for attr, value in location_data.items():
                setattr(location, attr, value)
            location.save()

        # Atualiza ou cria SocialMedia
        if social_media_data:
            if instance.social_media:
                social_media = instance.social_media
                for attr, value in social_media_data.items():
                    setattr(social_media, attr, value)
                social_media.save()
            else:
                social_media = SocialMedia.objects.create(**social_media_data)
                instance.social_media = social_media

        # Atualiza categorias
        if category_ids is not None:
            instance.category.set(category_ids)

        instance.save()
        return instance