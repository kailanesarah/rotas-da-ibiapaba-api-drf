from django.db import models
from accounts.models import Establishment


def upload_to_path(instance, filename):
    folder = instance.type_photo if instance.type_photo in ['profile', 'gallery', 'product'] else 'others'
    return f'photos/{instance.establishment.id}/{folder}/{filename}'

class Photo(models.Model):
    PROFILE = "profile"
    GALLERY = "gallery"
    PRODUCT = "product"

    PHOTO_TYPES = [
        (PROFILE, "Foto de Perfil"),
        (GALLERY, "Galeria"),
        (PRODUCT, "Produto"),
    ]

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name="Estabelecimento"
    )
    image = models.ImageField(upload_to=upload_to_path, blank=True, null=True)
    alt_text = models.CharField("Texto alternativo", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)
    type_photo = models.CharField("Tipo da foto", max_length=20, choices=PHOTO_TYPES)

    class Meta:
        indexes = [
            models.Index(fields=['establishment', 'type_photo']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['establishment'],
                condition=models.Q(type_photo='profile'),
                name='unique_profile_photo_per_establishment'
            )
        ]
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"

    def __str__(self):
        return f"{self.establishment.name} - {self.get_type_photo_display()}"

    @property
    def is_profile_pic(self):
        return self.type_photo == self.PROFILE

    @property
    def is_gallery_pic(self):
        return self.type_photo == self.GALLERY

    @property
    def is_product_pic(self):
        return self.type_photo == self.PRODUCT
