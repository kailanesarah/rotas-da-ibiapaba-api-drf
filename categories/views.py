from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.authentication import CookieJWTAuthentication
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoriesListCreateView(ListCreateAPIView):
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "message": f"Categorias listadas com sucesso.",
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        category_name = serializer.data.get("name", "Categoria")

        return Response(
            {
                "message": f"Categoria criada com sucesso.",
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# return Response({
#     "success": True,
#     "message": "Categoria criada com sucesso.",
#     "data": # {...} [...] ou null
# })
