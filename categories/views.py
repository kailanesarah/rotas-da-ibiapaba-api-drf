from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView
from rest_framework import status

from categories.models import Category
from categories.serializers import CategorySerializer  
from authentication.authentication import CookieJWTAuthentication


class CategoriesListCreateView(ListCreateAPIView):
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": {
                "title": "Categorias Listadas",
                "text": "Lista de categorias recuperada com sucesso.",
                "description": "Apresenta todas as categorias disponíveis no sistema, que pode ser paginada ou filtrada."
            },
            "success": True,
            "status": 200,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        category_name = serializer.data.get("name", "Categoria")

        return Response({
            "message": {
                "title": "Categoria Criada",
                "text": "A nova categoria foi cadastrada com sucesso.",
                "description": f"A categoria '{category_name}' foi adicionada ao sistema e já está disponível para uso."
            },
            "success": True,
            "status": 201,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
