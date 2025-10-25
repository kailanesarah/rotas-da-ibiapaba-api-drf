from django.contrib.auth import logout
from authentication.views.base import BaseAuthView
from authentication.utils.decorators import handle_exceptions
from authentication.utils.authentication import CookieJWTAuthentication


class LogoutView(BaseAuthView):
    authentication_classes = [CookieJWTAuthentication]

    @handle_exceptions
    def post(self, request):
        response = self.success("Logout realizado com sucesso")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        logout(request)
        return response
