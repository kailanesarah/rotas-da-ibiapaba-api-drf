from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    ValidationError,
    NotFound,
)
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from accounts.models import Establishment, User
from accounts.serializers.users_serializer import AdminUserCreateSerializer
from accounts.serializers.establishment_serializer import EstablishmentCreateUpdateSerializer
from authentication.authentication import CookieJWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST
)

from rest_framework import status


class EstablishmentListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentCreateUpdateSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        try:
            user = request.user
            
            if not hasattr(user, 'type') or user.type != 'admin':
                raise PermissionDenied("Você não tem permissão para acessar essa informação.")
            
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "message": {
                    "title": "Usuários Listados",
                    "text": "Lista de todos os usuários recuperada com sucesso.",
                },
                "success": True,
                "status": status.HTTP_200_OK,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": {
                    "title": "Erro ao listar usuários",
                    "text": str(e),
                },
                "success": False,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "message": {
                    "title": "Estabelecimento Registrado",
                    "text": "Seu novo estabelecimento foi cadastrado com sucesso.",
                },
                "success": True,
                "status": status.HTTP_201_CREATED,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                "message": {
                    "title": "Dados inválidos",
                    "text": e.detail,
                },
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message": {
                    "title": "Erro ao registrar estabelecimento",
                    "text": str(e),
                },
                "success": False,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentCreateUpdateSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_object(self):
        user = self.request.user  

        try:
            establishment = Establishment.objects.get(user=user)
            return establishment

        except Establishment.DoesNotExist:
            raise NotFound(detail="Estabelecimento não encontrado para este usuário.")

            return Response(
                {
                    "message": "Estabelecimento encontrado com sucesso.",
                    "success": True,
                    "data": establishment,
                },
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {
                    "message": "Estabelecimento não encontrado.",
                    "success": False,
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except AuthenticationFailed as auth_error:
            return Response(
                {
                    "message": f"Erro de autenticação - {str(auth_error)}",
                    "success": False,
                    "data": None,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        except PermissionDenied as permission_error:
            return Response(
                {
                    "message": f"Permissão negada - {str(permission_error)}",
                    "success": False,
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )


    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({
                "message": {
                    "title": "Dados do usuário atualizados com sucesso!",
                    "text": "As informações foram atualizadas corretamente.",
                },
                "success": True,
                "status": status.HTTP_200_OK,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": {
                    "title": "Erro ao atualizar os dados usuário",
                    "text": str(e),
                },
                "success": False,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                "message": {
                    "title": "Usuário excluído com sucesso",
                    "text": "Os dados do usuário serão excluídos de forma permanente em 30 dias. Caso queira reabrir a conta, entre em contato com nosso suporte. Abraços NexTech!",
                },
                "success": True,
                "status": status.HTTP_204_NO_CONTENT,
                "data": []
            }, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({
                "message": {
                    "title": "Erro ao excluir os dados usuário",
                    "text": str(e),
                },
                "success": False,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AdminListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(type='admin')
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "message": {
                    "title": "Admins Listados",
                    "text": "Lista de todos os administradores recuperada com sucesso.",
                },
                "success": True,
                "status": status.HTTP_200_OK,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": {
                    "title": "Erro ao listar administradores",
                    "text": str(e),
                },
                "success": False,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "message": {
                    "title": "Administrador Registrado",
                    "text": "Novo administrador cadastrado com sucesso.",
                },
                "success": True,
                "status": status.HTTP_201_CREATED,
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                "message": {
                    "title": "Dados inválidos",
                    "text": e.detail,
                },
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message": {
                    "title": "Erro ao registrar administrador",
                    "text": str(e),
                },
                "success": False,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
