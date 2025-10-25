from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from decouple import config


class EmailService:
    """
    Serviço responsável por enviar e-mails da aplicação Rotas da Ibiapaba.
    Oferece métodos genéricos para envio e suporte a templates HTML e texto.
    """

    def __init__(self):
        self.from_email = config("EMAIL_HOST_USER")

    def send_email(self, subject, body, user_email, html_template=None, context=None):

        try:
            if html_template:
                html_body = render_to_string(html_template, context or {})
                email = EmailMessage(
                    subject=subject,
                    body=html_body,
                    from_email=self.from_email,
                    to=[user_email],
                )
                email.content_subtype = "html"
            else:
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=self.from_email,
                    to=[user_email],
                )

            email.send(fail_silently=False)

        except Exception as e:
            raise Exception(f"Erro ao enviar e-mail: {str(e)}")

    def generate_email_encoded(self, email_user):
        """
        Codifica o e-mail do usuário para URLs seguras.
        """
        try:
            return urlsafe_base64_encode(force_bytes(email_user))
        except Exception as e:
            raise ValueError(f"Erro ao codificar e-mail: {str(e)}")

    def decode_email(self, encoded_email):
        """
        Decodifica um e-mail codificado via base64 seguro.
        """
        try:
            return force_str(urlsafe_base64_decode(encoded_email))
        except Exception:
            raise ValueError("Email inválido")
