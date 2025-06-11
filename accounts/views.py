from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView
from accounts.models import Establishment
from accounts.serializers import EstablishementSerializer
from authentication.authentication import CookieJWTAuthentication


class EstablishmentListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Establishment.objects.all()
    serializer_class = EstablishementSerializer
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": {
                "title": "Usuários Listados",
                "text": "Lista de todos os usuários recuperada com sucesso.",
                "description": "Esta resposta exibe a lista completa de usuários cadastrados no sistema, sem filtros aplicados."
            },
            "success": True,
            "status": 200,
            "data": serializer.data
        })

    def create(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": {
                "title": "Estabelecimento Registrado",
                "text": "Seu novo estabelecimento foi cadastrado com sucesso.",
                "description": "Ele já está ativo e pronto para ser configurado. Acesse a área de gerenciamento para adicionar detalhes, serviços e horários de funcionamento."
            },
            "success": True,
            "status": 201,
            "data": serializer.data
        })
