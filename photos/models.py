from django.db import models
from accounts.models import Establishment


#retorna um caminho tipo: photos/{id_do_estabelecimento}/profile/{nome_do_arquivo} o mesmo para os demais
def upload_to_path(instance, filename):
    if instance.is_profile_pic:
        return f'photos/{instance.establishment.id}/profile/{filename}'
    elif instance.is_gallery_pic:
        return f'photos/{instance.establishment.id}/gallery/{filename}'
    elif instance.is_product_pic:
        return f'photos/{instance.establishment.id}/product/{filename}'
    return f'photos/{instance.establishment.id}/others/{filename}'


class Photo(models.Model):
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name='photos'  # Permite: estabelecimento.photos.all()
    )
    image = models.ImageField(upload_to=upload_to_path)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_profile_pic = models.BooleanField(default=False)
    is_gallery_pic = models.BooleanField(default=False)
    is_product_pic = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['establishment', 'is_profile_pic']),
            models.Index(fields=['establishment', 'is_gallery_pic']),
            models.Index(fields=['establishment', 'is_product_pic']),
        ]

