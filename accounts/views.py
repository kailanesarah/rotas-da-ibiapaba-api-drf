from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from accounts.models import Establishment, User
from accounts.serializers import EstablishementSerializer, AdminCreateSerializer
from authentication.authentication import CookieJWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied, AuthenticationFailed, ValidationError
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)
from rest_framework import status


class EstablishmentListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Establishment.objects.all()
    serializer_class = EstablishementSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        try:
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


class DetailEstablishment(RetrieveAPIView):
    serializer_class = EstablishementSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get_object(self):
        try:
            pk = self.kwargs.get("pk")
            print(pk)

            if self.request.user.id != pk:
                raise PermissionDenied(
                    detail="Você não tem permissão para acessar os dados de outro usuário.",
                    code=HTTP_403_FORBIDDEN
                )

            user = User.objects.get(id=pk)
            print(user)
            establishment = Establishment.objects.get(user=user)

            return establishment

        except User.DoesNotExist:
            raise NotFound(
                detail="Usuário não encontrado.",
                code=HTTP_400_BAD_REQUEST
            )
        except Establishment.DoesNotExist:
            raise NotFound(
                detail="Estabelecimento não encontrado para este usuário.",
                code=HTTP_400_BAD_REQUEST
            )
        except AuthenticationFailed as auth_error:
            raise auth_error
        except PermissionDenied as permission_error:
            raise permission_error


class AdminListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(type='admin')
    serializer_class = AdminCreateSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
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
