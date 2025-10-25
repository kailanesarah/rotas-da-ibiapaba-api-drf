from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers.users.admin_user_serializer import AdminUserCreateSerializer
from authentication.utils.authentication import CookieJWTAuthentication


class AdminDeleteView(DestroyAPIView):
    """Exclui o administrador autenticado."""

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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {
                    "message": "Administrador excluído com sucesso.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao excluir o administrador: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
