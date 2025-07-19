from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import User, Establishment


class TokenService:

    def authenticate_user(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(
                request=request, email=email, password=password)
            return user
        except Exception as e:
            raise Exception(f"Erro na autenticação do usuário: {str(e)}")

    def get_token(self, user):
        try:
            refresh = TokenObtainPairSerializer.get_token(user)
            access = refresh.access_token
            return {
                'access': str(access),
                'refresh': str(refresh),
            }
        except Exception as e:
            raise Exception(f"Erro ao gerar tokens JWT: {str(e)}")

    def generate_reset_token(self, user):
        try:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            return token
        except Exception as e:
            raise Exception(f"Erro ao gerar token de reset de senha: {str(e)}")

    def validate_reset_token(self, user, token):
        try:
            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                raise ValueError("Token inválido ou expirado")
        except Exception as e:
            raise Exception(
                f"Erro na validação do token de reset de senha: {str(e)}")

    def get_user_from_refresh_token(refresh_token_str):
        try:
            token = RefreshToken(refresh_token_str)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)

            if user.type == 'admin':
                return user

            elif user.type == 'establishment':
                establishment = Establishment.objects.filter(user=user).first()
                if not establishment:
                    raise AuthenticationFailed(
                        "Nenhum estabelecimento encontrado para esse usuário.")
                return establishment

            else:
                raise AuthenticationFailed("Tipo de usuário inválido.")

        except Exception as e:
            raise AuthenticationFailed(f"Error: {e}")
