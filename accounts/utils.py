from django.utils.text import slugify
from accounts.models import User
import os


class RelatedFieldExtractorAdmin:
    def get_field(self, obj, name_field):
        related_manager = getattr(obj, name_field)
        if hasattr(related_manager, 'all'):
            return ", ".join([str(item) for item in related_manager.all()])

class GenerateUniqueName:
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

    def rename_establishment_folders(instance_pk, old_username, new_username):
        if not old_username or old_username == new_username:
            return

        old_folder_name = f"{instance_pk}_{old_username}"
        new_folder_name = f"{instance_pk}_{new_username}"

        base_media_path = 'photos'
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