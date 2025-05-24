# from rest_framework.permissions import IsAuthenticated
from django.views import View
from django.http import HttpResponse

class LoginView(View):
    def get(self, request):
        return HttpResponse("Página de login")

class LogoutView(View):
    def get(self, request):
        return HttpResponse("Logout efetuado")
