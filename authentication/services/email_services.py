from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from decouple import config

class EmailService:

    def send_email(self, subject, body, user_email):
        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=config('EMAIL_HOST_USER'),
                to=[user_email]
            )
            email.send()
        except Exception as e:
            raise Exception(f"Erro ao enviar e-mail: {str(e)}")

    def generate_email_encoded(self, email_user):
        try:
            email_encoded = urlsafe_base64_encode(force_bytes(email_user))
            return email_encoded
        except Exception as e:
            raise ValueError(f"Erro ao codificar e-mail: {str(e)}")

    def decode_email(self, encoded_email):
        try:
            return force_str(urlsafe_base64_decode(encoded_email))
        except Exception:
            raise ValueError("Email inválido")
