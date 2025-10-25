from rest_framework.views import APIView
from utils.response_utils import api_response


class BaseAuthView(APIView):
    """
    Classe base para views de autenticação,
    com métodos auxiliares para respostas padronizadas.
    """

    def success(self, message="", data=None, status_code=200):
        return api_response(message, True, data, status_code)

    def fail(self, message="", data=None, status_code=400):
        return api_response(message, False, data, status_code)
