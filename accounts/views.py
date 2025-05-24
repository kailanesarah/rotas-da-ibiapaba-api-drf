from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from accounts.models import Establishment
from accounts.serializers import EstablishementSerializer

class EstablishmentListCreateView(ListCreateAPIView):
    permission_classes = IsAuthenticated
    queryset = Establishment.objects.all()
    serializer_class = EstablishementSerializer
