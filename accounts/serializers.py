from rest_framework import serializers
from accounts.models import Location, Establishment, User
from categories.models import Category
from categories.serializers import CategorySerializer


class AdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        filelds = fields = ['id', 'email', 'username', 'password']
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


class EstablishementSerializer(serializers.ModelSerializer):
    user = EstablishmentCreateSerializer()
    location = LocationSerializer()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    categories = CategorySerializer(
        many=True, read_only=True, source='category'
    )

    class Meta:
        model = Establishment
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        location_data = validated_data.pop('location')
        category_ids = validated_data.pop('category')

        if not isinstance(category_ids, list):
            category_ids = [category_ids]

        user = EstablishmentCreateSerializer.create(
            EstablishmentCreateSerializer(), validated_data=user_data)
        location = Location.objects.create(**location_data)
        establishment = Establishment.objects.create(
            user=user,
            location=location,
            **validated_data
        )

        establishment.category.set(category_ids)

        return establishment
