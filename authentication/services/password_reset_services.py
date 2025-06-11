from decouple import config

class PasswordResetService:

    def generate_reset_link(self, token, email_encoded):
        base_url = config("BASE_URL")
        return f"{base_url}?token={token}&email={email_encoded}"

    def validate_passwords(self, password1, password2):
        if password1 != password2:
            raise ValueError("As senhas não coincidem")
