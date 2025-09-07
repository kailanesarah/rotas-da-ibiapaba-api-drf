from rest_framework.exceptions import NotAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Chama o manipulador de exceções padrão do DRF primeiro
    response = exception_handler(exc, context)

    # Se a exceção for NotAuthenticated, personaliza a resposta
    if isinstance(exc, NotAuthenticated):
        custom_response_data = {
            "message": "Usuário não autenticado. Por favor, faça login para continuar.",
            "success": False,
            "data": None,
        }
        response.data = custom_response_data
        response.status_code = (
            HTTP_401_UNAUTHORIZED  # Define o status HTTP para 401 Unauthorized
        )

    return response
