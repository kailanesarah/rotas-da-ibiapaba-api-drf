from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models.user import User
from accounts.serializers.users.admin_user_serializer import AdminUserCreateSerializer
from authentication.utils.authentication import CookieJWTAuthentication


class AdminListView(ListAPIView):
    """Lista todos os administradores (apenas admin pode acessar)."""

    queryset = User.objects.filter(type="admin")
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            if request.user.type != "admin":
                return Response(
                    {
                        "message": "Apenas administradores podem visualizar esta lista.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao listar administradores: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
