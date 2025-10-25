from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models.establishment import Establishment
from accounts.serializers.establishment.establishment_detail_serializer import (
    EstablishmentDetailSerializer,
)
from authentication.utils.authentication import CookieJWTAuthentication


class EstablishmentListView(ListAPIView):
    """Lista todos os estabelecimentos (somente admin)."""

    queryset = Establishment.objects.all()
    serializer_class = EstablishmentDetailSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            if request.user.type != "admin":
                return Response(
                    {
                        "message": "Acesso negado. Apenas administradores podem listar estabelecimentos.",
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
                    "message": f"Erro ao listar estabelecimentos: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
