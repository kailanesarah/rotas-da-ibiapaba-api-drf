from authentication.views.base import BaseAuthView
from authentication.utils.decorators import handle_exceptions
from authentication.services.auth.verification_services import VerificationService
from authentication.services.auth.password_reset.password_reset_service import (
    PasswordResetService,
)
from authentication.services.emails.email_services import EmailService
from authentication.services.emails.handler_template import send_password_reset


verification_service = VerificationService()
password_reset_service = PasswordResetService()
email_service = EmailService()


class PasswordResetView(BaseAuthView):

    @handle_exceptions
    def post(self, request):
        email_user = request.data.get("email")
        user = verification_service.get_user_by_email(email_user)

        token = password_reset_service.generate_reset_token(user)
        email_encoded = email_service.generate_email_encoded(user.email)
        reset_url = password_reset_service.generate_reset_link(token, email_encoded)

        send_password_reset(user_email=user.email, reset_link=reset_url)

        return self.success(
            f"Link de redefinição de senha enviado para o e-mail: {user.email}"
        )
