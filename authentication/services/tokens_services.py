from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenService:

    def authenticate_user(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request=request, email=email, password=password)
        return user

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    def generate_reset_token(self, user):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        return token

    def validate_reset_token(self, user, token):
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise ValueError("Token inválido ou expirado")
