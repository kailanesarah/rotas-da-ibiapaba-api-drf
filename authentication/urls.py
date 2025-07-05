from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    CodeValidatorView,
    PasswordResetView,
    PasswordResetConfirmView,
    ResendCodeView,
)

urlpatterns = [
    # JWT Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  
    # Autenticação
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),

    # Validação de código
    path('verify_code/', CodeValidatorView.as_view(), name='verify_code_view'),
    path('resend_code/', ResendCodeView.as_view(), name='resend_code_view'),

    # Redefinição de senha
    path('reset_password/', PasswordResetView.as_view(), name='reset_password_view'),
    path('reset_confirm_password/', PasswordResetConfirmView.as_view(), name='confirm_password_view'),
]
