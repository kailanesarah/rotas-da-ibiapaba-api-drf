import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Establishment, Location
from categories.models import Category

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, db):
    user = User.objects.create_user(
        username="John Doe",
        email="john@gmail.com",
        password="password123",
        type="admin",
    )
    api_client.force_authenticate(user=user)
    return user


@pytest.fixture
def create_user_for_establishment(db):
    return User.objects.create_user(
        username="owner",
        email="owner@example.com",
        password="password123",
        type="establishment",
    )


@pytest.fixture
def create_location(db):
    return Location.objects.create(
        country="Brasil",
        state="CE",
        city="Fortaleza",
        CEP="60000000",
        neighborhood="Centro",
        street="Rua dos Testes",
        number=123,
    )


@pytest.fixture
def create_category(db):
    return Category.objects.create(name="Serviços")


@pytest.fixture
def create_establishment(
    db, create_user_for_establishment, create_location, create_category
):
    establishment = Establishment.objects.create(
        user=create_user_for_establishment,
        name="Barbearia do Zé",
        CNPJ="12345678000195",
        whatsapp=85999998888,
        location=create_location,
    )
    establishment.category.add(create_category)
    return establishment


@pytest.mark.integration
class TestEstablishmentListCreateView:
    """Verifica se um usuário autenticado PODE listar estabelecimentos."""

    def test_list_establishments_authenticated(
        self, api_client, authenticated_user, create_establishment
    ):
        url = reverse("establishment_create_list_view")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["name"] == "Barbearia do Zé"

    def test_create_establishment_success(
        self,
        api_client,
        create_user_for_establishment,
        create_location,
        create_category,
    ):
        url = reverse("establishment_create_list_view")

        establishment_data = {
            "name": "Salão da Maria",
            "CNPJ": "98765432000100",
            "whatsapp": 88988887777,
            "user": {
                "username": "maria_owner",
                "email": "maria@example.com",
                "password": "password123",
                "type": "establishment",
            },
            "location": {
                "country": "Brasil",
                "state": "PI",
                "city": "Teresina",
                "CEP": "64000000",
                "neighborhood": "Centro",
                "street": "Rua Nova",
                "number": 456,
            },
            "category": [create_category.id],
        }
        response = api_client.post(url, establishment_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["message"]["title"] == "Estabelecimento Registrado"

        assert Establishment.objects.filter(name="Salão da Maria").exists()

    def test_create_establishment_with_invalid_user(
        self,
        api_client,
        create_user_for_establishment,
        create_location,
        create_category,
    ):
        url = reverse("establishment_create_list_view")

        establishment_data = {
            "name": "Salão da Maria",
            "CNPJ": "98765432000100",
            "whatsapp": 88988887777,
            "user": {
                "username": "maria_owner",
                "email": "maria@example.com",
                "password": "password123",
                "type": "admin",  # <-- Invalid User
            },
            "location": {
                "country": "Brasil",
                "state": "PI",
                "city": "Teresina",
                "CEP": "64000000",
                "neighborhood": "Centro",
                "street": "Rua Nova",
                "number": 456,
            },
            "category": [create_category.id],
        }
        response = api_client.post(url, establishment_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
