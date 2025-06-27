import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from categories.models import Category

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, db):
    user = User.objects.create_user(
        username="John Doe", email="john@gmail.com", password="password123"
    )
    api_client.force_authenticate(user=user)
    return user


@pytest.fixture
def create_categories(db):
    Category.objects.create(name="Hotel")
    Category.objects.create(name="Restourante")


class TestCategoriesListCreateView:

    def test_list_categories_authenticated(
        self, api_client, authenticated_user, create_categories
    ):

        url = reverse("categories_create_list_view")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]) == 2
        assert response.data["data"][0]["name"] == "Hotel"

    def test_list_categories_unauthenticated(self, api_client):
        url = reverse("categories_create_list_view")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_category_success(self, api_client, db):

        url = reverse("categories_create_list_view")
        category_data = {"name": "Passeio"}
        initial_count = Category.objects.count()

        response = api_client.post(url, category_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["data"]["name"] == category_data["name"]
        assert Category.objects.count() == initial_count + 1

    def test_create_category_invalid_data(self, api_client, db):
        url = reverse("categories_create_list_view")
        invalid_data = {"name": ""}
        initial_count = Category.objects.count()
        response = api_client.post(url, invalid_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Category.objects.count() == initial_count
