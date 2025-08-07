from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    ValidationError,
)
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from accounts.models import Establishment, User
from accounts.serializers import AdminCreateSerializer, EstablishmentSerializer
from authentication.authentication import CookieJWTAuthentication


class EstablishmentListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "Usuários listados com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao listar usuários - {str(e)}",
                    "success": False,
                    "data": [],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {
                    "message": "Estabelecimento registrado com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            return Response(
                {
                    "message": f"Dados inválidos - {e.detail}",
                    "success": False,
                    "data": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao registrar estabelecimento - {str(e)}",
                    "success": False,
                    "data": [],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DetailEstablishment(RetrieveAPIView):
    serializer_class = EstablishmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_object(self):
        try:
            pk = self.kwargs.get("pk")

            if self.request.user.id != pk:
                raise PermissionDenied(
                    detail="Você não tem permissão para acessar os dados de outro usuário.",
                    code=status.HTTP_403_FORBIDDEN,
                )

            user = User.objects.get(id=pk)
            establishment = Establishment.objects.get(user=user)

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


class AdminListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(type="admin")
    serializer_class = AdminCreateSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "Administradores listados com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao listar administradores - {str(e)}",
                    "success": False,
                    "data": [],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {
                    "message": f"Novo administrador registrado com sucesso.",
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            return Response(
                {
                    "message": f"Dados inválidos - {e.detail}",
                    "success": False,
                    "data": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao registrar administrador - {str(e)}",
                    "success": False,
                    "data": [],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
