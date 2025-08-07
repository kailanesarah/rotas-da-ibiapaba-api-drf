from django.core.management.base import BaseCommand

from accounts.models import Establishment, Location, SocialMedia, User
from categories.models import Category


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):

        self.stdout.write("Limpando o banco de dados...")
        # Limpa os dados existentes para evitar duplicatas
        Establishment.objects.all().delete()
        Category.objects.all().delete()
        Location.objects.all().delete()
        SocialMedia.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Criação de categorias
        category_hotel = Category.objects.create(name="Hotel")
        category_restaurant = Category.objects.create(name="Restaurante")
        category_tourist_spot = Category.objects.create(name="Ponto Turístico")

        self.stdout.write("Categorias criadas com sucesso.")

        # Criação da localização Viçosa do Ceará
        location_vicosa = Location.objects.create(
            country="Brasil",
            state="CE",
            city="Viçosa do Ceará",
            CEP="62300000",
            neighborhood="Centro",
            street="Rua Principal",
            number=100,
        )

        # Criar midia social - Hotel
        social_media_hotel = SocialMedia.objects.create(
            whatsapp="88912345678", instagram="@hotelvistalinda"
        )

        # Criação do usuário Estabelecimento do Hotel
        user_establishment_hotel = User.objects.create_user(
            username="hotelvistalinda",
            email="contato@hotelvistalinda.com",
            password="password123",
            type="establishment",
        )

        # Criação do estabelecimento Hotel Vista Linda
        establishment_hotel = Establishment.objects.create(
            user=user_establishment_hotel,
            name="Hotel Vista Linda",
            description="O melhor hotel da serra.",
            cnpj="11222333000144",
            location=location_vicosa,
            social_media=social_media_hotel,
        )
        establishment_hotel.category.add(category_hotel, category_tourist_spot)

        # Criação localisação Tianguá
        location_tiangua = Location.objects.create(
            country="Brasil",
            state="CE",
            city="Tianguá",
            CEP="62320000",
            neighborhood="Centro",
            street="Avenida Central",
            number=250,
        )

        # Criar midia social - Restaurante
        social_media_restaurant = SocialMedia.objects.create(
            whatsapp="88987654321", instagram="@restaurantebomgosto"
        )

        user_establishment_restaurant = User.objects.create_user(
            username="sabordaserra",
            email="contato@sabordaserra.com",
            password="password123",
            type="establishment",
        )

        establishment_restaurant = Establishment.objects.create(
            user=user_establishment_restaurant,
            name="Restaurante Sabor da Serra",
            description="Comida regional de alta qualidade.",
            cnpj="44555666000177",
            location=location_tiangua,
            social_media=social_media_restaurant,
        )
        establishment_restaurant.category.add(category_restaurant)

        self.stdout.write(self.style.SUCCESS("Banco de dados semeado com sucesso!"))
