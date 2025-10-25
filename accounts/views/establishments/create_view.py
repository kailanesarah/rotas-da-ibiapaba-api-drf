from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models.establishment import Establishment
from accounts.serializers.establishment.establishment_create_update_serializer import (
    EstablishmentCreateUpdateSerializer,
)
from accounts.serializers.establishment.establishment_detail_serializer import (
    EstablishmentDetailSerializer,
)
from authentication.utils.authentication import CookieJWTAuthentication


class EstablishmentCreateView(CreateAPIView):
    """Cria um novo estabelecimento (público)."""

    queryset = Establishment.objects.all()
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        """
        Retorna o serializer adequado conforme a ação:
        - POST: cria/atualiza (entrada de dados)
        - GET: detalha (saída de dados)
        """
        if self.request.method == "POST":
            return EstablishmentCreateUpdateSerializer
        return EstablishmentDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            # Após criar, usa o serializer de leitura para retornar o objeto completo
            detail_serializer = EstablishmentDetailSerializer(serializer.instance)
            return Response(
                {
                    "data": detail_serializer.data,
                    "message": "Estabelecimento criado com sucesso.",
                },
                status=status.HTTP_201_CREATED,
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
                    "message": f"Erro inesperado ao criar o estabelecimento: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
