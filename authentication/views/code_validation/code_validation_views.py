from rest_framework import status
from authentication.views.base import BaseAuthView
from authentication.utils.decorators import handle_exceptions
from authentication.utils.cookie_utils import set_tokens_in_response
from accounts.models import Establishment, User
from accounts.serializers.establishment.establishment_create_update_serializer import (
    EstablishmentCreateUpdateSerializer,
)
from authentication.services.auth.tokens.token_service import TokenService
from authentication.services.auth.cookies.cookie_service import CookieService
from authentication.services.auth.verification_services import VerificationService

token_service = TokenService()
verification_service = VerificationService()
cookie_service = CookieService()


class CodeValidatorView(BaseAuthView):

    @handle_exceptions
    def post(self, request):
        email_user = request.data.get("email")
        code_user = request.data.get("code")

        user = verification_service.get_user_by_email(email_user)
        user_obj = User.objects.get(email=email_user)
        establishment = Establishment.objects.filter(user=user_obj).first()

        if verification_service.verify_code(code_user, email_user) == 0:
            return self.fail(
                "Código incorreto, tente novamente",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        tokens = token_service.get_token(user)
        access_token, refresh_token = tokens["access"], tokens["refresh"]

        response_data = {}
        if establishment:
            serializer = EstablishmentCreateUpdateSerializer(establishment)
            response_data = {"user_type": "establishment", "user": serializer.data}
        else:
            response_data = {
                "user_type": getattr(user, "type", None),
                "user": {"id": user.id, "email": user.email},
            }

        response = self.success("Usuário autenticado com sucesso!", data=response_data)
        return set_tokens_in_response(
            response, access_token, refresh_token, cookie_service
        )
