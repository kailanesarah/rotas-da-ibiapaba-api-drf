from rest_framework.generics import ListCreateAPIView
from accounts.models import Establishment
from accounts.serializers import EstablishementSerializer

class EstablishmentListCreateView(ListCreateAPIView):
    queryset = Establishment.objects.all()
    serializer_class = EstablishementSerializer
