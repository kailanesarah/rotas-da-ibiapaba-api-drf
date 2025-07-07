from django.urls import path
from accounts.views import EstablishmentListCreateView, AdminListCreateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('establishment/', EstablishmentListCreateView.as_view(),name="establishment_create_list_view"),
    path('admin/', AdminListCreateView.as_view(), name='admin_create_list_view')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
