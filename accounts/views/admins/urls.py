from django.urls import path
from accounts.views.admins import (
    AdminListView,
    AdminCreateView,
    AdminRetrieveView,
    AdminUpdateView,
    AdminDeleteView,
)

urlpatterns = [
    path("", AdminListView.as_view(), name="admin-list"),
    path("create/", AdminCreateView.as_view(), name="admin-create"),
    path("me/", AdminRetrieveView.as_view(), name="admin-retrieve"),
    path("me/update/", AdminUpdateView.as_view(), name="admin-update"),
    path("me/delete/", AdminDeleteView.as_view(), name="admin-delete"),
]
