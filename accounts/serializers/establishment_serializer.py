from rest_framework import serializers
from accounts.models import Establishment, User, Location, SocialMedia
from categories.models import Category
from categories.serializers import CategorySerializer
from accounts.serializers.users_serializer import EstablishmentUserCreateSerializer
from accounts.serializers.location_serializer import LocationSerializer
from accounts.serializers.social_media_serializer import SocialMediaSerializer
from accounts.utils import UniqueUsernameGenerator,UsernameUtils
from photos.utils import PhotoUtils


class EstablishmentUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email', 'username']


class EstablishmentCreateUpdateSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()
    gallery_photos = serializers.SerializerMethodField()
    product_photos = serializers.SerializerMethodField()

    def get_profile_photo(self, obj):
        return PhotoUtils.get_photo_url_by_type(obj.photos, 'profile')

    def get_gallery_photos(self, obj):
        return PhotoUtils.get_multiple_photo_urls_by_types(obj.photos, ['gallery'])

    def get_product_photos(self, obj):
        return PhotoUtils.get_multiple_photo_urls_by_types(obj.photos, ['product'])


    # Campo usado apenas para criar o usuário (escrita)
    user = serializers.DictField(write_only=True)

    # Informações do usuário exibidas em respostas (leitura)
    user_info = EstablishmentUserInfoSerializer(source='user', read_only=True)

    # Localização e redes sociais (aninhados)
    location = LocationSerializer()
    social_media = SocialMediaSerializer(required=False)

    # Categorias (escrita com IDs e leitura com dados completos)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True
    )
    categories = CategorySerializer(
        many=True,
        read_only=True,
        source='category'
    )
    
    # Campos que chamam os métodos acima para retornar URLs das fotos
    profile_photo = serializers.SerializerMethodField()
    gallery_photos = serializers.SerializerMethodField()


    class Meta:
        model = Establishment
        fields = [
            'id','user', 'user_info',
            'name', 'description', 'cnpj',
            'social_media', 'location',
            'category', 'categories',
            'pix_key', 'profile_photo', 
            'gallery_photos', 'product_photos'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        location_data = validated_data.pop('location')
        social_media_data = validated_data.pop('social_media', None)
        category_ids = validated_data.pop('category')

        # Gera username a partir do nome do estabelecimento
        base_name = validated_data.get('name', 'estabelecimento')
        username = UniqueUsernameGenerator().generate_unique_username(base_name)
        user_data['username'] = username

        # Verifica duplicidade de email
        email = user_data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Este e-mail já está em uso.'})

        # Cria usuário com serializer especializado 
        user_serializer = EstablishmentUserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Cria localização
        location = Location.objects.create(**location_data)

        # Cria redes sociais
        social_media = None
        if social_media_data:
            social_media = SocialMedia.objects.create(**social_media_data)

        # Cria estabelecimento vinculando usuário, localização e redes sociais
        establishment = Establishment.objects.create(
            user=user,
            location=location,
            social_media=social_media,
            **validated_data
        )

        # Associa categorias ao estabelecimento
        establishment.category.set(category_ids)

        return establishment


    def update(self, instance, validated_data):
        # Extrai dados aninhados, se existirem
        user_data = validated_data.pop('user', None)
        location_data = validated_data.pop('location', None)
        social_media_data = validated_data.pop('social_media', None)
        category_ids = validated_data.pop('category', None)

        old_username = instance.user.username
        old_name = instance.name
        new_name = validated_data.get('name')

        UsernameUtils().update_rename_folder(instance, old_username, new_name)

        # Atualiza dados do usuário
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                if attr == 'password':
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()

        # Atualiza localização
        if location_data:
            location = instance.location
            for attr, value in location_data.items():
                setattr(location, attr, value)
            location.save()

        # Atualiza redes sociais
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

        # Atualiza demais campos do estabelecimento
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
