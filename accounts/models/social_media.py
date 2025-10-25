from django.db import models


class SocialMedia(models.Model):
    """Redes sociais do estabelecimento."""

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Número do WhatsApp com DDD, ex: (88) 9 11999999",
    )
    instagram = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Usuário do Instagram ex: @joao_silva",
    )
    facebook = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Usuário do Facebook ex: joao_silva",
    )

    def __str__(self):
        return self.instagram or self.whatsapp or "Sem redes sociais"
