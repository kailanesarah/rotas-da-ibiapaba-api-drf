import pytest

from authentication.services.password_reset_services import PasswordResetService


@pytest.mark.unit
class TestPasswordResetService:

    @pytest.fixture
    def password_reset_service(self):
        return PasswordResetService()

    def test_generate_password_reset_link_correctly(self, password_reset_service):
        base_url = "http://rotas-da-ibiapaba-frontend.vercel.app/reset_password"
        token = "reset_token"
        encoded_email = "encoded_email_base64"

        success_url = f"{base_url}?token={token}&email={encoded_email}"

        response = password_reset_service.generate_reset_link(token, encoded_email)

        assert response == success_url

    def test_validade_passwords_raise_error(self, password_reset_service):
        password_1 = "password 1"
        password_2 = "password 2"

        with pytest.raises(ValueError, match="As senhas não coincidem"):
            password_reset_service.validate_passwords(password_1, password_2)
