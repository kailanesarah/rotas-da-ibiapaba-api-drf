from unittest.mock import MagicMock, patch

import pytest

from authentication.services.email_services import EmailService


@pytest.mark.integration
class TestEmailSending:
    @pytest.fixture
    def email_service(self):
        return EmailService()

    @patch("authentication.services.email_services.EmailMessage")
    def test_email_calls_email_message_correctly(
        self, mock_email_message_class, email_service
    ):
        subject = "Assunto do teste"
        body = "Corpo do email de teste"
        user_email = "john@gmail.com"
        from_email = "nextechbusiness24@gmail.com"

        mock_instance = MagicMock()
        mock_email_message_class.return_value = mock_instance

        email_service.send_email(subject, body, user_email)

        mock_email_message_class.assert_called_once()

        mock_email_message_class.assert_called_with(
            subject=subject, body=body, from_email=from_email, to=[user_email]
        )

        mock_instance.send.assert_called_once()


@pytest.mark.unit
class TestEmailEncoding:

    @pytest.fixture
    def email_service(self):
        return EmailService()

    def test_generate_and_decode_email_successfully(self, email_service):

        original_email = "john@gmail.com"

        encoded_email = email_service.generate_email_encoded(original_email)
        decoded_email = email_service.decode_email(encoded_email)

        assert isinstance(encoded_email, str)
        assert encoded_email != original_email
        assert decoded_email == original_email

    def test_decode_email_raise_value_error(self, email_service):

        invalid_encoded_string = "invalid encoded email"

        with pytest.raises(ValueError, match="Email inválido"):
            email_service.decode_email(invalid_encoded_string)
