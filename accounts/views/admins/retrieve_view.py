from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models.user import User
from accounts.serializers.users.admin_user_serializer import AdminUserCreateSerializer
from authentication.utils.authentication import CookieJWTAuthentication


class AdminRetrieveView(RetrieveAPIView):
    """Recupera os dados do administrador autenticado."""

    serializer_class = AdminUserCreateSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            user = self.request.user
            if user.type != "admin":
                raise NotFound("Administrador não encontrado ou sem permissão.")
            return user
        except Exception as e:
            raise NotFound(f"Erro ao localizar administrador: {str(e)}")

    def retrieve(self, request, *args, **kwargs):
        try:
            admin = self.get_object()
            serializer = self.get_serializer(admin)
            return Response(
                {
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao recuperar administrador: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
