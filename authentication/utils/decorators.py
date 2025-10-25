from functools import wraps
from utils.response_utils import api_response


def handle_exceptions(func):
    """
    Captura exceções em views e retorna resposta padronizada.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return api_response(
                message="Erro ao processar a requisição.",
                success=False,
                data=str(e),
                status_code=400,
            )

    return wrapper
