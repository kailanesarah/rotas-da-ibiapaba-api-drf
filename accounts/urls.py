
from django.contrib import admin
from django.urls import path,include
from accounts.views import EstablishmentListCreateView

urlpatterns = [
    path('auth/register/', EstablishmentListCreateView.as_view(), name="establishment_List_Create_View"),

]

