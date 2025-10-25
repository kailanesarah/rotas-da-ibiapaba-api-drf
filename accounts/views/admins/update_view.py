from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers.users.admin_user_serializer import AdminUserCreateSerializer
from authentication.utils.authentication import CookieJWTAuthentication


class AdminUpdateView(UpdateAPIView):
    """Atualiza os dados do administrador autenticado."""

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

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            return Response(
                {
                    "message": f"Erro de validação nos dados enviados: {str(e)}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro inesperado ao atualizar o administrador: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
