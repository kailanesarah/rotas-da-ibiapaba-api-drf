from authentication.views.base import BaseAuthView
from authentication.utils.decorators import handle_exceptions
from authentication.services.auth.verification_services import VerificationService
from authentication.services.emails.handler_template import (
    resend_verification_code,
)

verification_service = VerificationService()


class ResendCodeView(BaseAuthView):

    @handle_exceptions
    def post(self, request):
        email_user = request.data.get("email")
        user = verification_service.get_user_by_email(email_user)

        code = verification_service.generate_code()
        verification_service.save_code(code, user.email)

        # Envia o código usando template
        resend_verification_code(user_email=user.email, code=code)

        return self.success(
            f"Código reenviado com sucesso para o usuário: {email_user}"
        )
