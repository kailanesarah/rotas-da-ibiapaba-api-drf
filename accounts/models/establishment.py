from django.db import models
from categories.models import Category
from accounts.models.user import User
from accounts.models.location import Location
from accounts.models.social_media import SocialMedia
from accounts.utils.id_utils import IDGenerator


def generate_establishment_id():
    return IDGenerator.generate("E")


class Establishment(models.Model):
    """Representa um estabelecimento comercial."""

    id = models.CharField(
        primary_key=True,
        default=generate_establishment_id,
        max_length=10,
        editable=False,
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="establishment_user"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True)

    social_media = models.ForeignKey(
        SocialMedia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="establishments_social_media",
    )

    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="establishment_location"
    )

    category = models.ManyToManyField(Category, related_name="establishments_category")

    pix_key = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Chave Pix (e-mail, telefone, CPF/CNPJ ou aleatória)",
    )

    def __str__(self):
        return self.name

    # Métodos utilitários
    def get_profile_photo(self):
        return self.photos.filter(type_photo="profile").first()

    def get_gallery_photos(self):
        return self.photos.filter(type_photo="gallery")

    def get_product_photos(self):
        return self.photos.filter(type_photo="product")
