from rest_framework import serializers
from accounts.models import Location, Establishment, User, SocialMedia
from categories.models import Category
from categories.serializers import CategorySerializer
from photos.serializers import EstablishmentProfileImageSerializer
from photos.models import EstablishmentProfileImage


class AdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        filelds = ['id', 'email', 'username', 'password']
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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'


class EstablishementSerializer(serializers.ModelSerializer):
    user = EstablishmentCreateSerializer()
    location = LocationSerializer()
    social_media = SocialMediaSerializer()
    photo = EstablishmentProfileImageSerializer(read_only=True)

    # entrada de dados
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )

    # para leitura de dados
    categories = CategorySerializer(
        many=True, read_only=True, source='category'
    )

    class Meta:
        model = Establishment
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        location_data = validated_data.pop('location')
        social_media_data = validated_data.pop('social_media', None)
        photo_data = validated_data.pop('photo', None)
        category_ids = validated_data.pop('category')

        # Criar usuário e localização
        user = EstablishmentCreateSerializer.create(
            EstablishmentCreateSerializer(), validated_data=user_data)
        location = Location.objects.create(**location_data)

        # Criar social_media se existir
        social_media = None
        if social_media_data:
            social_media = SocialMedia.objects.create(**social_media_data)

        # Criar o estabelecimento
        establishment = Establishment.objects.create(
            user=user,
            location=location,
            social_media=social_media,
            **validated_data
        )

        # Associar categorias
        establishment.category.set(category_ids)

        # Criar foto se existir e associar
        if photo_data:
            photo = EstablishmentProfileImage.objects.create(**photo_data)
            establishment.photo = photo
            establishment.save()

        return establishment
