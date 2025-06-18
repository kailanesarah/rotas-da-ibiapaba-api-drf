from django.urls import path
from categories.views import CategoriesListCreateView

urlpatterns = [
    path('categorie/', CategoriesListCreateView.as_view(), name="categories_create_list_view"),
]

