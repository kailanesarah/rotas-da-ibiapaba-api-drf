from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
