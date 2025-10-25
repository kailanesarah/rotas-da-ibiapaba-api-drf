from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models.user import User
from accounts.serializers.users.admin_user_serializer import AdminUserCreateSerializer
from authentication.utils.authentication import CookieJWTAuthentication


class AdminCreateView(CreateAPIView):
    """
    Cria um novo administrador (público ou sob autorização futura).
    """

    queryset = User.objects.filter(type="admin")
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return AdminUserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {
                    "data": serializer.data,
                    "message": "Administrador criado com sucesso.",
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            return Response(
                {"message": f"Erro de validação nos dados enviados: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"message": f"Erro inesperado ao criar administrador: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
