from django.urls import path
from categories.views import CategoriesListCreateView

urlpatterns = [
    path('register/', CategoriesListCreateView.as_view(), name="categories_Create_View"),
    path('list/', CategoriesListCreateView.as_view(), name="categories_List_View"),
]

