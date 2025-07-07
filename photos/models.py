from django.db import models


class EstablishmentProfileImage(models.Model):
    image = models.ImageField(
        upload_to='profile_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Texto alternativo para acessibilidade"
    )
