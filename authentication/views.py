from django.contrib.auth import logout, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated
from app.utils import AuthenticationMethods
from accounts.models import User
from authentication.authentication import CookieJWTAuthentication


class CodeValidatorView(APIView):

    def post(self, request):
        try:
            auth_methods = AuthenticationMethods()
            
            email_user = request.data.get('email')
            code_user = request.data.get('code')

            # Verifica código
            code_verification_result = auth_methods.verify_code(code_user, email_user)
            if code_verification_result == 0:
                return Response(
                {'error': 'Código incorreto, tente novamente'}, 
                status=HTTP_401_UNAUTHORIZED
                )
                
            # Busca usuário
            try:
                user = User.objects.get(email=email_user)
            except User.DoesNotExist:
                return Response(
                    {'error': 'Usuário não encontrado'}, 
                    status=HTTP_404_NOT_FOUND)

            try:
                # Gera tokens
                tokens = auth_methods.get_token(user)
                access_token = tokens['access']
                refresh_token = tokens['refresh']

                # Prepara resposta
                response = Response({
                    'success': 'Código verificado com sucesso',
                    'user_id': user.id,
                    'email': user.email
                }, status=HTTP_200_OK)

                # Cria cookies para os tokens
                auth_methods.create_cookie(response, 'access_token', access_token, 3* 4)  # 15 min
                auth_methods.create_cookie(response, 'refresh_token', refresh_token, 7 * 24 * 60 * 60)  # 7 dias

                return response

            except KeyError as e:
                # Caso algum token não esteja na resposta
                return Response(
                    {'error': f'Token não encontrado na resposta: {str(e)}'},
                    status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response({
                'error': 'Erro na tentativa de validar o codigo', 
                'detail': str(e)
                }, status=HTTP_400_BAD_REQUEST)


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
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication] 
    
    def post(self, request):
        try:
            #Prepara response
            response = Response({'success': 'Logout realizado com sucesso'}, status=HTTP_200_OK)
            
            # Deleta os cookies do token
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            logout(request)  
            
            return response  
        except Exception as e:
            return Response({'error': 'Erro ao fazer logout', 'detail': str(e)}, status=HTTP_400_BAD_REQUEST)
