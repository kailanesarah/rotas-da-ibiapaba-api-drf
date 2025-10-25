from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models.establishment import Establishment
from accounts.serializers.establishment.establishment_create_update_serializer import (
    EstablishmentCreateUpdateSerializer,
)
from authentication.utils.authentication import CookieJWTAuthentication


class EstablishmentDeleteView(DestroyAPIView):
    """Exclui o estabelecimento do usuário autenticado."""

    serializer_class = EstablishmentCreateUpdateSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Establishment.objects.get(user=self.request.user)
        except Establishment.DoesNotExist:
            raise NotFound("Estabelecimento não encontrado para este usuário.")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {
                    "message": "Estabelecimento excluído com sucesso.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "message": f"Erro ao excluir o estabelecimento: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
