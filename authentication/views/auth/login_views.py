from django.contrib.auth import login
from authentication.views.base import BaseAuthView
from authentication.utils.decorators import handle_exceptions
from authentication.services.auth.tokens.authentication_service import (
    AuthenticationService,
)
from authentication.services.auth.verification_services import VerificationService
from authentication.services.emails.handler_template import (
    send_verification_code,
)

authentication_service = AuthenticationService()
verification_service = VerificationService()


class LoginView(BaseAuthView):

    @handle_exceptions
    def post(self, request):
        user = authentication_service.authenticate_user(request)
        if not user:
            return self.fail("Credenciais inválidas. Tente novamente", status_code=401)

        login(request, user)

        # Gerar e salvar código de verificação
        code = verification_service.generate_code()
        verification_service.save_code(code, user.email)

        # Enviar e-mail usando o template
        send_verification_code(user_email=user.email, code=code)

        return self.success("Código enviado para seu e-mail. Verifique para continuar")
