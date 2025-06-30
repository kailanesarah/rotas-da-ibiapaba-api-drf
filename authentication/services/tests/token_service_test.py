import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from authentication.services.tokens_services import TokenService

User = get_user_model()

pytestmark = [pytest.mark.integration, pytest.mark.django_db]


@pytest.fixture
def token_service():
    return TokenService()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="John Doe", email="john@gmail.com", password="password123"
    )


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


class TestTokenService:

    def test_authenticate_user_success(self, token_service, user, api_request_factory):

        data = {"email": "john@gmail.com", "password": "password123"}

        wsgi_request = api_request_factory.post("/fake-login/", data)
        drf_request = APIView().initialize_request(wsgi_request)

        authenticated_user = token_service.authenticate_user(drf_request)

        assert authenticated_user is not None
        assert authenticated_user == user

    def test_authenticate_user_with_wrong_password(
        self, token_service, user, api_request_factory
    ):

        data = {"email": "john@gmail.com", "password": "wrong-password"}

        wsgi_request = api_request_factory.post("/fake-login/", data)
        drf_request = APIView().initialize_request(wsgi_request)

        authenticated_user = token_service.authenticate_user(drf_request)

        assert authenticated_user is None

    def test_get_token_returns_correct_struture(self, token_service, user):

        tokens = token_service.get_token(user)

        assert isinstance(tokens, dict)
        assert "access" in tokens
        assert "refresh" in tokens
        assert isinstance(tokens["access"], str)
        assert isinstance(tokens["refresh"], str)

    def test_generate_and_validate_token_round_trip(self, token_service, user):

        token = token_service.generate_reset_token(user)

        try:
            token_service.validate_reset_token(user, token)

        except ValueError:
            pytest.fail("A validação do token falhou inesperadamente.")

    def test_validate_token_raises_erro(self, token_service, user):

        invalid_token = "invalid_token"

        with pytest.raises(ValueError, match="Token inválido ou expirado"):
            token_service.validate_reset_token(user, invalid_token)
