from accounts.models import User
from django.core.cache import cache
import pyotp
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
)


class VerificationService:

    def generate_code(self):
        code = pyotp.TOTP(pyotp.random_base32(), interval=300, digits=5)
        return code.now()

    def save_code(self, code, user_email):
        chave = f"code_{user_email}"
        cache.set(chave, code, timeout=300)  # 5 minutos

    def verify_code(self, code, user_email):
        code_stored = cache.get(f"code_{user_email}")
        if code_stored == code:
            return 1
        return 0

    def get_user_by_email(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"}, status=HTTP_404_NOT_FOUND
            )
