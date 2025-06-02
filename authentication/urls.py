from django.urls import path
from .views import LoginView, LogoutView, CodeValidatorView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='login_view'),
    path('verifyCode/', CodeValidatorView.as_view(), name='login_view'),
]
