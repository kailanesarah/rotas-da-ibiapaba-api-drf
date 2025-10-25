from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models.establishment import Establishment
from accounts.serializers.establishment.establishment_detail_serializer import (
    EstablishmentDetailSerializer,
)
from authentication.utils.authentication import CookieJWTAuthentication


class EstablishmentRetrieveView(RetrieveAPIView):
    """Recupera o estabelecimento do usuário autenticado."""

    serializer_class = EstablishmentDetailSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Establishment.objects.get(user=self.request.user)
        except Establishment.DoesNotExist:
            raise NotFound("Estabelecimento não encontrado para este usuário.")

    def retrieve(self, request, *args, **kwargs):
        try:
            establishment = self.get_object()
            serializer = self.get_serializer(establishment)
            return Response(
                {
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao recuperar o estabelecimento: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
