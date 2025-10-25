from django.contrib.auth import authenticate


class AuthenticationService:

    def authenticate_user(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            user = authenticate(request=request, email=email, password=password)
            return user
        except Exception as e:
            raise Exception(f"Erro na autenticação do usuário: {str(e)}")
