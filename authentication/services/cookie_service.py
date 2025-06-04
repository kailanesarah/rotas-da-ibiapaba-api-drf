from django.conf import settings

class CookieService:
    
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