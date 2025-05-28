from django.contrib.auth import authenticate, logout, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken
from app.utils import AuthenticationMethods
from accounts.models import User


class CodeValidatorView(APIView):

    def post(self, request):
        try:
            auth_methods = AuthenticationMethods()
            email_user = self.request.data.get('email')
            code_user = self.request.data.get('code')

            response = auth_methods.verify_code(code_user, email_user)

            if response == 0:
                return Response({'error': 'Código incorreto, tente novamente'}, status=401)

            try:
                user = User.objects.get(email=email_user)
            except User.DoesNotExist:
                return Response({'error': 'Usuário não encontrado'}, status=404)

            tokens = auth_methods.get_token(user)

            return Response({
            'success': 'Código verificado com sucesso',
            'tokens': tokens,
            'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
            }
            }, status=200)
        except Exception as e:
            return Response({'error': 'Erro na tentativa de validar o codigo', 'detail': str(e)}, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        try:
            auth_methods = AuthenticationMethods()
            user = auth_methods.authenticate_user(request)

            if user:
                login(request, user)
                code = auth_methods.generate_code()
                auth_methods.save_code(code, user.email)
                auth_methods.send_email(code, user.email)

                return Response({
                    'message': 'Código enviado para seu e-mail. Verifique para continuar.'
                }, status=HTTP_200_OK)

            return Response({'error': 'Credenciais inválidas'}, status=HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'error': 'Erro ao fazer login', 'detail': str(e)}, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)

            return Response({'success': 'Logout realizado com sucesso'}, status=HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Erro ao fazer logout', 'detail': str(e)}, status=HTTP_400_BAD_REQUEST)
