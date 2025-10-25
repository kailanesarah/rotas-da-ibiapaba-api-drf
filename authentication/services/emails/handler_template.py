from authentication.services.emails.email_services import EmailService

email_service = EmailService()


def send_verification_code(user_email, code):
    """
    Envia o código de verificação para o usuário.
    """
    subject = "Código de Verificação - Rotas da Ibiapaba"
    email_service.send_email(
        subject=subject,
        body=None,
        user_email=user_email,
        html_template="verification_code_template.html",
        context={"code": code},
    )


def resend_verification_code(user_email, code):
    """
    Reenvia o código de verificação para o usuário.
    """
    subject = "Reenvio de Código - Rotas da Ibiapaba"
    email_service.send_email(
        subject=subject,
        body=None,
        user_email=user_email,
        html_template="resend_code_template.html",
        context={"code": code},
    )


def send_password_reset(user_email, reset_link):
    """
    Envia o link de redefinição de senha para o usuário.
    """
    subject = "Redefinição de Senha - Rotas da Ibiapaba"
    email_service.send_email(
        subject=subject,
        body=None,
        user_email=user_email,
        html_template="password_reset_template.html",
        context={"link": reset_link},
    )
