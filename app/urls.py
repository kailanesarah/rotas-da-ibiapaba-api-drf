
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('authentication.urls')), #Urls que geram o token e o refresh | login | logout
    path('api/accounts/', include('accounts.urls')), #Cria e lista usuarios
]

