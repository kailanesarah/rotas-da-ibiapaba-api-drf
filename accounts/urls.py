from django.urls import path
from accounts.views import EstablishmentListCreateView, AdminListCreateView

urlpatterns = [
    path('establishment/', EstablishmentListCreateView.as_view(), name="establishment_Create_List_View"),
    path('admin/', AdminListCreateView.as_view(), name='create_admin')
]

