import pytest
from django.conf import settings as django_settings
from django.http import HttpResponse

from authentication.services.cookie_service import CookieService


@pytest.mark.unit
class TesteCookieService:

    @pytest.fixture
    def cookie_service(self):
        return CookieService()

    def test_create_cookie_in_debug_mode(self, cookie_service):
        response = HttpResponse()
        key = "auth_key"
        value = "secret_value"
        max_age = 3600  # 1 hora

        modified_response = cookie_service.create_cookie(response, key, value, max_age)

        assert modified_response is response

        assert key in response.cookies

        cookie = response.cookies[key]
        assert cookie.value == value
        assert cookie["max-age"] == max_age
        assert cookie["httponly"] is True
        assert cookie["samesite"] == "Lax"
        assert cookie["path"] == "/"

    def test_create_cookie_in_poduction_mode(self, cookie_service, settings):

        # Alteramos temporariamente a configuraçãos para simular ambiente de produção
        settings.DEBUG = False

        response = HttpResponse()
        key = "auth_key"
        value = "secret_value"
        max_age = 3600  # 1 hora

        modified_response = cookie_service.create_cookie(response, key, value, max_age)

        assert key in response.cookies

        cookie = response.cookies[key]

        assert cookie["secure"] is True
        assert cookie.value == value
        assert cookie["max-age"] == max_age
        assert cookie["httponly"] is True
