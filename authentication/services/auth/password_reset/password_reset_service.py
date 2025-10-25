from django.contrib.auth.tokens import PasswordResetTokenGenerator
from decouple import config


class PasswordResetService:

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
            raise Exception(f"Erro na validação do token de reset de senha: {str(e)}")

    def generate_reset_link(self, token, email_encoded):
        try:
            base_url = config("URL_FRONT")
            return f"{base_url}?token={token}&email={email_encoded}"
        except Exception as e:
            raise Exception(f"Erro ao gerar link de redefinição de senha: {str(e)}")

    def validate_passwords(self, password1, password2):
        try:
            if password1 != password2:
                raise ValueError("As senhas não coincidem")
        except Exception as e:
            raise Exception(f"Erro na validação das senhas: {str(e)}")
