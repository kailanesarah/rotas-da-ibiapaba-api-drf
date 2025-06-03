import random
from django.core.mail import EmailMessage
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
import pyotp

class RelatedFieldExtractorAdmin:
    def get_field(self, obj, name_field):
        related_manager = getattr(obj, name_field)
        if hasattr(related_manager, 'all'):
            return ", ".join([str(item) for item in related_manager.all()])


class AuthenticationMethods:

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

    def generate_code(self):
        code = pyotp.TOTP(pyotp.random_base32(), interval=300)
        return code.now()

    def save_code(self, code, user_email):
        chave = f'code_{user_email}'
        cache.set(chave, code, timeout=300)  # 5 minutos

    def verify_code(self, code, user_email):
        code_stored = cache.get(f'code_{user_email}')
        if code_stored == code:
            return 1
        return 0

    def send_email(self, code, user_email):
        email = EmailMessage(
            subject="Bem-vindo ao Rotas da Ibiapaba!",
            body= 
            (
                f"Olá, tudo bem? Bem-vindo ao Rotas da Ibiapaba!\n"
                "Aqui nós cuidamos para que a sua experiência seja única e inesquecível.\n\n"
                f"Seu código de acesso é: {code}"
            ),
            from_email = "nextechbusiness24@gmail.com",
            to=[user_email]
        )
        email.send()
        
        
    def create_cookie(self, response, key_cookie, value_cookie, max_age_cookie):
        response.set_cookie(
            key=key_cookie,
            value=value_cookie,
            httponly=True,
            secure=not settings.DEBUG,         # só em produção com HTTPS
            samesite='Lax',
            max_age= max_age_cookie , 
            path='/'
        )
        
        return response

    
    
    

