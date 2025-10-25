from rest_framework.response import Response


def api_response(message="", success=True, data=None, status_code=200):
    """
    Retorna uma resposta padronizada para a API.
    """
    return Response(
        {"message": message, "success": success, "data": data},
        status=status_code,
    )
