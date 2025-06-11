from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

class EmailService:
    
    def send_email(self, subject, body, user_email, ):
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email = "nextechbusiness24@gmail.com",
            to=[user_email]
        )
        email.send()
        
    def generate_email_encoded(self, email_user):
        email_encoded = urlsafe_base64_encode(force_bytes(email_user))
        return  email_encoded
    
    def decode_email(self, encoded_email):
        try:
            return force_str(urlsafe_base64_decode(encoded_email))
        except Exception:
            raise ValueError("Email inválido")