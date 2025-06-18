from django.urls import path
from accounts.views import EstablishmentListCreateView, AdminListCreateView

urlpatterns = [
    path('establishment/', EstablishmentListCreateView.as_view(), name="establishment_create_list_view"),
    path('admin/', AdminListCreateView.as_view(), name='admin_create_list_view')
]

