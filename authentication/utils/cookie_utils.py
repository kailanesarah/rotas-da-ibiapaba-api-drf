def set_tokens_in_response(response, access_token, refresh_token, cookie_service):
    """
    Cria cookies de access e refresh token na resposta.
    """
    duration = 7 * 24 * 60 * 60  # 7 dias
    cookie_service.create_cookie(response, "access_token", access_token, duration)
    cookie_service.create_cookie(response, "refresh_token", refresh_token, duration)
    return response
