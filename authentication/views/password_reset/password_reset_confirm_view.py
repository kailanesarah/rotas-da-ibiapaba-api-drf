from authentication.views.base import BaseAuthView
from authentication.utils.decorators import handle_exceptions
from authentication.services.auth.verification_services import VerificationService
from authentication.services.auth.password_reset.password_reset_service import (
    PasswordResetService,
)
from authentication.services.emails.email_services import EmailService

password_reset_service = PasswordResetService()
verification_service = VerificationService()
email_service = EmailService()


class PasswordResetConfirmView(BaseAuthView):

    @handle_exceptions
    def patch(self, request):
        email_encoded = request.data.get("email")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        email = email_service.decode_email(email_encoded)
        user = verification_service.get_user_by_email(email)

        password_reset_service.validate_reset_token(user, token)

        user.set_password(new_password)
        user.save()

        return self.success(f"Senha redefinida com sucesso para o usuário: {email}")
