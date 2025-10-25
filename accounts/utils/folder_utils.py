import os
from django.conf import settings


class EstablishmentFolderRenamer:
    """Renomeia as pastas de mídia associadas a um estabelecimento."""

    @staticmethod
    def rename_folders(instance_pk: int, old_username: str, new_username: str):
        if not old_username or old_username == new_username:
            return

        old_folder_name = f"{instance_pk}_{old_username}"
        new_folder_name = f"{instance_pk}_{new_username}"
        base_media_path = os.path.join(settings.MEDIA_ROOT, "photos")
        folders = ["profile", "gallery", "product", "others"]

        for folder in folders:
            old_path = os.path.join(base_media_path, folder, old_folder_name)
            new_path = os.path.join(base_media_path, folder, new_folder_name)

            if os.path.exists(old_path):
                print(f"Pasta encontrada: {old_path}")

                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renomeado: {old_path} → {new_path}")
                else:
                    print(
                        f"A pasta destino {new_path} já existe. Renomeação não feita."
                    )
            else:
                print(f"Pasta {old_path} não encontrada. Nada foi feito.")
