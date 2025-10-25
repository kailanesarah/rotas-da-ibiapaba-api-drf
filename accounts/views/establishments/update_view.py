from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models.establishment import Establishment
from accounts.serializers.establishment.establishment_create_update_serializer import (
    EstablishmentCreateUpdateSerializer,
)
from accounts.serializers.establishment.establishment_detail_serializer import (
    EstablishmentDetailSerializer,
)
from authentication.utils.authentication import CookieJWTAuthentication


class EstablishmentUpdateView(UpdateAPIView):
    """Atualiza os dados do estabelecimento do usuário autenticado."""

    serializer_class = EstablishmentCreateUpdateSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Establishment.objects.get(user=self.request.user)
        except Establishment.DoesNotExist:
            raise NotFound("Estabelecimento não encontrado para este usuário.")

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            # Retorna o objeto atualizado com o serializer de leitura
            detail_serializer = EstablishmentDetailSerializer(instance)
            return Response(
                {
                    "data": detail_serializer.data,
                    "message": "Estabelecimento atualizado com sucesso.",
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
                    "message": f"Erro inesperado ao atualizar o estabelecimento: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
