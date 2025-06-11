from django.urls import path
from accounts.views import EstablishmentListCreateView

urlpatterns = [
    path('register/', EstablishmentListCreateView.as_view(), name="establishment_Create_View"),
    path('list/', EstablishmentListCreateView.as_view(), name="establishment_List_View"),
]

