from django.contrib import admin
from accounts.models import Establishment

@admin.register(Establishment)
class EstablishmentAdmin():
    list_diplay = '__all__'

