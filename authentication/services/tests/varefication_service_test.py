import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from authentication.services.auth.verification_services import VerificationService

User = get_user_model()


@pytest.fixture(autouse=True)
def clean_cache():
    cache.clear()
    yield


@pytest.fixture
def verification_service():
    return VerificationService()


@pytest.fixture
@pytest.mark.django_db
def user():
    return User.objects.create_user(username="John Doe", email="john@gmail.com")


@pytest.mark.unit
class TestVerificationService:

    def test_generate_code_returns_string(self, verification_service):
        code = verification_service.generate_code()

        assert isinstance(code, str)
        assert len(code) == 6

    def test_save_and_verify_code_round_trip(self, verification_service):

        user_email = "john@email.com"
        code = "123456"

        verification_service.save_code(code, user_email)
        result = verification_service.verify_code(code, user_email)

        assert result == 1

    def test_verify_wrong_code_fails(self, verification_service):

        user_email = "john@email.com"
        correct_code = "123456"
        wrong_code = "678912"

        verification_service.save_code(correct_code, user_email)
        result = verification_service.verify_code(wrong_code, user_email)

        assert result == 0

    def test_verify_non_existent_code_fails(self, verification_service):

        user_email = "user@example.com"
        code = "123456"

        result = verification_service.verify_code(code, user_email)

        assert result == 0

    @pytest.mark.django_db
    def test_get_user_by_email_success(self, verification_service, user):

        found_user = verification_service.get_user_by_email("john@gmail.com")

        assert found_user is not None
        assert found_user == user

    @pytest.mark.django_db
    def test_get_user_by_email_not_found(self, verification_service):

        result = verification_service.get_user_by_email("nonexistent@gmail.com")

        assert isinstance(result, Response)
        assert result.status_code == status.HTTP_404_NOT_FOUND
        assert result.data["error"] == "Usuário não encontrado"
