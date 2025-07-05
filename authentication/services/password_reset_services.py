from decouple import config
class PasswordResetService:

    def generate_reset_link(self, token, email_encoded):
        try:
            base_url = config('URL_FRONT')
            return f"{base_url}?token={token}&email={email_encoded}"
        except Exception as e:
            raise Exception(f"Erro ao gerar link de redefinição de senha: {str(e)}")

    def validate_passwords(self, password1, password2):
        try:
            if password1 != password2:
                raise ValueError("As senhas não coincidem")
        except Exception as e:
            raise Exception(f"Erro na validação das senhas: {str(e)}")
