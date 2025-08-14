from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from accounts.models import Establishment, User
from accounts.serializers.establishment_serializer import (
    EstablishmentCreateUpdateSerializer,
)
from accounts.serializers.users_serializer import AdminUserCreateSerializer
from authentication.authentication import CookieJWTAuthentication


class EstablishmentListCreateView(ListCreateAPIView):
    """
    View para listar todos os estabelecimentos (apenas admin) ou criar um novo.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentCreateUpdateSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        # Permite que qualquer um crie um estabelecimento (ex: durante o cadastro)
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        # Garante que apenas usuários administradores possam listar os estabelecimentos.
        if not hasattr(request.user, "type") or request.user.type != "admin":
            return Response(
                {
                    "message": "Você não tem permissão para acessar este recurso.",
                    "success": False,
                    "data": None,
                },
                status=HTTP_403_FORBIDDEN,
            )

        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "Lista de estabelecimentos recuperada com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao listar estabelecimentos: {str(e)}",
                    "success": False,
                    "data": None,
                },
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Seu novo estabelecimento foi cadastrado com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response(
                {
                    "message": "Dados inválidos fornecidos.",
                    "success": False,
                    "data": e.detail,
                },
                status=HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao registrar o estabelecimento: {str(e)}",
                    "success": False,
                    "data": None,
                },
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EstablishmentRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    View para recuperar, atualizar ou deletar o estabelecimento do usuário autenticado.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentCreateUpdateSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_object(self):
        """Retorna o estabelecimento associado ao usuário autenticado."""
        user = self.request.user

        try:
            establishment = Establishment.objects.get(user=user)
            return Response(
                {
                    "message": "Estabelecimento encontrado com sucesso.",
                    "success": True,
                    "data": establishment,
                },
                status=HTTP_200_OK,
            )

        except Establishment.DoesNotExist:
            raise NotFound(detail="Estabelecimento não encontrado para este usuário.")

        except User.DoesNotExist:
            return Response(
                {
                    "message": "Estabelecimento não encontrado.",
                    "success": False,
                    "data": None,
                },
                status=HTTP_400_BAD_REQUEST,
            )

        except AuthenticationFailed as auth_error:
            return Response(
                {
                    "message": f"Erro de autenticação - {str(auth_error)}",
                    "success": False,
                    "data": None,
                },
                status=HTTP_401_UNAUTHORIZED,
            )

        except PermissionDenied as permission_error:
            return Response(
                {
                    "message": f"Permissão negada - {str(permission_error)}",
                    "success": False,
                    "data": None,
                },
                status=HTTP_403_FORBIDDEN,
            )

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(
                {
                    "message": "Dados do estabelecimento atualizados com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao atualizar os dados do estabelecimento: {str(e)}",
                    "success": False,
                    "data": None,
                },
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {
                    "message": "Estabelecimento excluído com sucesso.",
                    "success": True,
                    "data": None,
                },
                status=HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao excluir o estabelecimento: {str(e)}",
                    "success": False,
                    "data": None,
                },
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(type="admin")
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "Lista de administradores recuperada com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao listar administradores: {str(e)}",
                    "success": False,
                    "data": None,
                },
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {
                    "message": "Administrador registrado com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=HTTP_201_CREATED,
            )

        except ValidationError as e:
            return Response(
                {
                    "message": "Dados inválidos fornecidos.",
                    "success": False,
                    "data": e.detail,
                },
                status=HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao registrar o administrador: {str(e)}",
                    "success": False,
                    "data": None,
                },
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
