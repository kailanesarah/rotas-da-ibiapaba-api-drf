from rest_framework import status
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView

from authentication.authentication import CookieJWTAuthentication
from authentication.services.cookie_service import CookieService
from authentication.services.email_services import EmailService
from authentication.services.password_reset_services import PasswordResetService
from authentication.services.tokens_services import TokenService
from authentication.services.verification_services import VerificationService

from accounts.serializers.establishment_serializer import EstablishmentCreateUpdateSerializer
from accounts.models import Establishment, User

# instancias
token_service = TokenService()
verification_service = VerificationService()
email_service = EmailService()
password_reset_service = PasswordResetService()
cookie_service = CookieService()


class CodeValidatorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email_user = request.data.get("email")
            code_user = request.data.get("code")

            # Verifica usuário pelo email
            user = verification_service.get_user_by_email(email_user)
            user_obj = User.objects.get(email=email_user)
            establishment = Establishment.objects.filter(user=user_obj).first()

            # Verifica código
            code_verification_result = verification_service.verify_code(
                code_user, email_user
            )
            if code_verification_result == 0:
                return Response(
                    {'error': 'Código incorreto, tente novamente'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                # Gera tokens
                tokens = token_service.get_token(user)
                access_token = tokens["access"]
                refresh_token = tokens["refresh"]

                # Cria resposta vazia
                response = Response(status=200)

                # User: Estabelecimento
                if establishment:
                    establishment_serializer = EstablishmentCreateUpdateSerializer(
                        establishment)
                    response.data = {
                        'success': 'Usuário autenticado com sucesso!',
                        'user_type': 'establishment',
                        'user': establishment_serializer.data
                    }
                else:
                    # User:Admin
                    if hasattr(user, 'type'):
                        response.data = {
                            'success': 'Usuário autenticado com sucesso!',
                            'user_type': user.type,
                            'user': {
                                'id': user.id,
                                'email': user.email
                            }
                        }

                # Cria cookies para os tokens
                cookie_service.create_cookie(
                    response, 'access_token', access_token, 7 * 24 * 60 * 60)
                cookie_service.create_cookie(
                    response, 'refresh_token', refresh_token, 7 * 24 * 60 * 60)

                return response

            except KeyError as e:
                return Response(
                    {'error': f'Token não encontrado na resposta: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            return Response({
                'error': 'Erro na tentativa de validar o código',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = token_service.authenticate_user(request)

            if user:
                login(request, user)
                code = verification_service.generate_code()
                verification_service.save_code(code, user.email)

                subject = "Bem vindo ao Rotas da Ibiapaba!"
                body = (
                    "Olá!\n\n"
                    "Seja bem-vindo ao Rotas da Ibiapaba, a plataforma que te ajuda a explorar o melhor da nossa região!\n\n"
                    "Use este código para fazer seu primeiro login e aproveitar todos os recursos disponíveis.\n\n"
                    f"Seu código de acesso é: {code}\n\n"
                    "Se tiver alguma dúvida, estamos aqui para ajudar.\n\n"
                    "Equipe Rotas da Ibiapaba"
                )

                email_service.send_email(subject, body, user.email)

                return Response(
                    {
                        "message": "Código enviado para seu e-mail. Verifique para continuar."
                    },
                    status=HTTP_200_OK,
                )

            return Response(
                {"error": "Credenciais inválidas"}, status=HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            return Response(
                {"error": "Erro ao fazer login", "detail": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            response = Response(
                {"success": "Logout realizado com sucesso"}, status=HTTP_200_OK
            )
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            logout(request)
            return response
        except Exception as e:
            return Response(
                {"error": "Erro ao fazer logout", "detail": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email_user = request.data.get("email")
            user = verification_service.get_user_by_email(email_user)

            # codifica o email e gera tokens
            email_encoded = email_service.generate_email_encoded(user.email)
            token = token_service.generate_reset_token(user)
            reset_url = password_reset_service.generate_reset_link(token, email_encoded)

            # envia link email
            subject = "Redefinição de senha - Rotas da Ibiapaba"
            body = (
                "Olá!\n\n"
                "Recebemos uma solicitação para redefinir a sua senha da plataforma Rotas da Ibiapaba.\n\n"
                f"Para continuar com a redefinição, acesse o link abaixo:\n\n"
                f"{reset_url}\n\n"
                "Se você não solicitou essa alteração, por favor, ignore esta mensagem.\n\n"
                "Estamos à disposição para ajudar no que for necessário.\n\n"
                "Equipe Rotas da Ibiapaba"
            )

            email_service.send_email(subject, body, user.email)

            return Response(
                {"sucesso": "Solicitação de reset feita com sucesso"},
                status=HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": "Erro ao processar solicitação", "detail": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        try:
            email_encoded = request.data.get("email")
            token = request.data.get("token")
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            # Decodifica o email
            email = email_service.decode_email(email_encoded)
            user = verification_service.get_user_by_email(email)

            # Valida senhas e token
            password_reset_service.validate_passwords(new_password, confirm_password)
            token_service.validate_reset_token(user, token)

            # atualiza senha
            user.set_password(new_password)
            user.save()

            return Response(
                {"message": f"Senha redefinida com sucesso para o usuário: {email}"},
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Erro ao processar a requisição", "detail": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )


class ResendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email_user = request.data.get("email")
            user = verification_service.get_user_by_email(email_user)

            code = verification_service.generate_code()
            verification_service.save_code(code, user.email)

            subject = "NexTech: Seu novo código chegou!"
            body = (
                f"Olá novamente!\n\n"
                "Conforme solicitado, aqui está um novo código de acesso para que você possa entrar no *Rotas da Ibiapaba* e continuar explorando o melhor da nossa região!\n\n"
                f"*Seu novo código de acesso:* {code}\n\n"
                "Caso não tenha solicitado este código, basta ignorar esta mensagem.\n\n"
                "Se precisar de ajuda, conte com a gente!\n\n"
                "Atenciosamente,\n"
                "Equipe Rotas da Ibiapaba "
            )

            email_service.send_email(subject, body, user.email)
            return Response({'message': f'Código reenviado com sucesso para o usuário: {email_user}'}, status=HTTP_200_OK)

        except Exception as e:

            return Response({'error': 'Erro ao processar a requisição', 'detail': str(e)}, status=HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            if not refresh_token:
                raise AuthenticationFailed('Refresh token não encontrado.')

            serializer = TokenRefreshSerializer(
                data={'refresh': refresh_token})
            serializer.is_valid(raise_exception=True)

            new_access_token = serializer.validated_data['access']
            new_refresh_token = serializer.validated_data['refresh']

            # Cria resposta padrão
            response = Response(status=200)

            # Define novos cookies
            cookie_service.create_cookie(
                response, 'access_token', new_access_token, 7 * 24 * 60 * 60
            )
            cookie_service.create_cookie(
                response, 'refresh_token', new_refresh_token, 7 * 24 * 60 * 60
            )

            # Recupera usuário dono do refresh token
            user = TokenService.get_user_from_refresh_token(new_refresh_token)

            # User: Admin
            if hasattr(user, 'type') and user.type == 'admin':
                response.data = {
                    'success': 'Tokens atualizados',
                    'user_type': 'admin',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    }
                }
                return response

            # User: Estabelecimento
            elif hasattr(user, 'name'):
                try:
                    establishment_serializer = EstablishmentSerializer(user)
                    response.data = {
                        'success': 'Tokens atualizados',
                        'user_type': 'establishment',
                        'user': establishment_serializer.data
                    }
                    return response
                except Establishment.DoesNotExist:
                    return Response(
                        {'error': 'Estabelecimento não encontrado para este usuário.'},
                        status=404
                    )

            # Se tipo não reconhecido
            return Response(
                {'error': 'Tipo de usuário não reconhecido'},
                status=400
            )

        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(
                {'error': 'Erro ao atualizar tokens', 'detail': str(e)},
                status=HTTP_400_BAD_REQUEST
            )
