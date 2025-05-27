from django.contrib.auth import authenticate, logout, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):

    def post(self, request):

        try:
            email = self.request.data.get('email')
            password = self.request.data.get('password')
            user = authenticate(
                request=request, email=email, password=password)

            if user:
                login(request, user)  # inicia uma seção
                refresh = RefreshToken.for_user(user)  # gera um token

                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }}, status=HTTP_200_OK)
            return Response({'success': 'Logout realizado com sucesso'}, status=HTTP_200_OK)
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
