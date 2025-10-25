from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.exceptions import AuthenticationFailed
from authentication.views.base import BaseAuthView
from authentication.utils.decorators import handle_exceptions
from authentication.utils.cookie_utils import set_tokens_in_response
from authentication.services.auth.tokens.token_service import TokenService
from accounts.models import Establishment
from accounts.serializers.establishment.establishment_create_update_serializer import (
    EstablishmentCreateUpdateSerializer,
)

token_service = TokenService()


class TokenRefreshView(BaseAuthView):

    @handle_exceptions
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            raise AuthenticationFailed("Refresh token não encontrado.")

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        new_access_token = serializer.validated_data["access"]
        new_refresh_token = serializer.validated_data["refresh"]

        user = TokenService.get_user_from_refresh_token(new_refresh_token)

        response_data = {}

        if hasattr(user, "type") and user.type == "admin":
            response_data = {
                "user_type": "admin",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            }

        elif hasattr(user, "name"):
            establishment = Establishment.objects.filter(user=user).first()
            if establishment:
                serializer = EstablishmentCreateUpdateSerializer(establishment)
                response_data = {"user_type": "establishment", "user": serializer.data}

            else:
                return self.fail(
                    "Estabelecimento não encontrado para este usuário", status_code=404
                )

        else:
            return self.fail("Tipo de usuário não reconhecido", status_code=400)

        response = self.success("Tokens atualizados", data=response_data)
        return set_tokens_in_response(
            response, new_access_token, new_refresh_token, token_service.cookie_service
        )
