from django.urls import path
from accounts.views.establishments import (
    EstablishmentListView,
    EstablishmentCreateView,
    EstablishmentRetrieveView,
    EstablishmentUpdateView,
    EstablishmentDeleteView,
)

urlpatterns = [
    path("", EstablishmentListView.as_view(), name="establishment-list"),
    path("create/", EstablishmentCreateView.as_view(), name="establishment-create"),
    path("me/", EstablishmentRetrieveView.as_view(), name="establishment-retrieve"),
    path("me/update/", EstablishmentUpdateView.as_view(), name="establishment-update"),
    path("me/delete/", EstablishmentDeleteView.as_view(), name="establishment-delete"),
]
