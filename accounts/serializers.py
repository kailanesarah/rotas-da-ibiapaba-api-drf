from rest_framework import serializers
from accounts.models import Category, Location, Establishment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            type=validated_data['type'],  # <-- importante!
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class EstablishementSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    location = LocationSerializer()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True)  
    
    categories = CategorySerializer(many=True, read_only=True, source='category')

    class Meta:
        model = Establishment
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        location_data = validated_data.pop('location')
        category_ids = validated_data.pop('category')

        if not isinstance(category_ids, list):
            category_ids = [category_ids]

        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        location = Location.objects.create(**location_data)
        establishment = Establishment.objects.create(
            user=user,
            location=location,
            **validated_data
        )
      
        establishment.category.set(category_ids)

        return establishment
