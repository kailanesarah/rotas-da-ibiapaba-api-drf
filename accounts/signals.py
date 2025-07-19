from django.db.models.signals import pre_save
from accounts.models import Establishment
from django.dispatch import receiver
from django.utils.text import slugify
import os

@receiver(pre_save, sender=Establishment)
def rename_establishment_folder(sender, instance, **kwargs):

    old_instance = Establishment.objects.get(pk=instance.pk)

    old_name = old_instance.name
    new_name = instance.name

    old_slug = slugify(old_name)
    new_slug = slugify(new_name)

    base_media_path = 'photos'
    folders = ['profile', 'gallery', 'product', 'others']

    for folder in folders:
        old_path = os.path.join(base_media_path, folder, old_slug)
        new_path = os.path.join(base_media_path, folder, new_slug)

        try:
            if os.path.exists(old_path):
                print(f"Pasta encontrada: {old_path}")

                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renomeado: {old_path} → {new_path}")
                else:
                    print(
                        f"A pasta destino {new_path} já existe. Renomeação não feita.")
            else:
                print(f"Pasta {old_path} não encontrada. Nada foi feito.")
        except Exception as e:
            print(
                f"Erro ao tentar renomear a pasta {old_path} para {new_path}: {e}")
