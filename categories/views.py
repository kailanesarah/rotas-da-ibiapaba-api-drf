from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from authentication.utils.authentication import CookieJWTAuthentication
from categories.models import Category
from categories.serializers import CategorySerializer
from utils.response_utils import api_response


class CategoriesListCreateView(ListCreateAPIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            message="Categorias listadas com sucesso.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(
            message="Categoria criada com sucesso.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )
