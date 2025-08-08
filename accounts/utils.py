import os
from django.utils.text import slugify
from django.conf import settings
from accounts.models import User
import shortuuid


class IDGenerator:
    @staticmethod
    def gerar_id_amigavel(tamanho=8):
        su = shortuuid.ShortUUID(
            alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        return su.random(length=tamanho)


class RelatedFieldExtractorAdmin:
    @staticmethod
    def get_field(obj, name_field):
        related_manager = getattr(obj, name_field, None)
        if related_manager and hasattr(related_manager, 'all'):
            return ", ".join([str(item) for item in related_manager.all()])
        return ""


class UniqueUsernameGenerator:
    @staticmethod
    def generate_unique_username(base_name):
        username = slugify(base_name).replace('-', '_')
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1
            if counter > 100:
                raise ValueError("Não foi possível gerar um username único")
        return username


class EstablishmentFolderRenamer:
    @staticmethod
    def rename_folders(instance_pk, old_username, new_username):
        if not old_username or old_username == new_username:
            return

        old_folder_name = f"{instance_pk}_{old_username}"
        new_folder_name = f"{instance_pk}_{new_username}"

        base_media_path = os.path.join(settings.MEDIA_ROOT, 'photos')
        folders = ['profile', 'gallery', 'product', 'others']

        for folder in folders:
            old_path = os.path.join(base_media_path, folder, old_folder_name)
            new_path = os.path.join(base_media_path, folder, new_folder_name)

            if os.path.exists(old_path):
                print(f"Pasta encontrada: {old_path}")

                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renomeado: {old_path} → {new_path}")
                else:
                    print(f"A pasta destino {new_path} já existe. Renomeação não feita.")
            else:
                print(f"Pasta {old_path} não encontrada. Nada foi feito.")


from django.utils.text import slugify
from django.contrib.auth import get_user_model

class UsernameUtils:
    @staticmethod
    def update_rename_folder(instance, old_name: str, new_name: str):
        if new_name and new_name != old_name:
            slugified_name = slugify(new_name).replace('-', '_')
            new_username = slugified_name

            UserModel = get_user_model()
            original_username = new_username
            counter = 1
            while UserModel.objects.filter(username=new_username).exclude(pk=instance.user.pk).exists():
                new_username = f"{original_username}_{counter}"
                counter += 1

            instance.user.username = new_username
            instance.user.save()

            EstablishmentFolderRenamer.rename_folders(
                instance.pk,
                old_username=old_name,
                new_username=new_username
            )
