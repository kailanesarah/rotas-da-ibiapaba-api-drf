from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import User, Establishment


class TokenService:

    def get_token(self, user):
        try:
            refresh = TokenObtainPairSerializer.get_token(user)
            access = refresh.access_token
            return {
                "access": str(access),
                "refresh": str(refresh),
            }
        except Exception as e:
            raise Exception(f"Erro ao gerar tokens JWT: {str(e)}")

    @staticmethod
    def get_user_from_refresh_token(refresh_token_str):
        try:
            token = RefreshToken(refresh_token_str)
            user_id = token["user_id"]
            user = User.objects.get(id=user_id)

            if user.type == "admin":
                return user
            elif user.type == "establishment":
                establishment = Establishment.objects.filter(user=user).first()
                if not establishment:
                    raise AuthenticationFailed(
                        "Nenhum estabelecimento encontrado para esse usuário."
                    )
                return establishment
            else:
                raise AuthenticationFailed("Tipo de usuário inválido.")
        except Exception as e:
            raise AuthenticationFailed(f"Error: {e}")
