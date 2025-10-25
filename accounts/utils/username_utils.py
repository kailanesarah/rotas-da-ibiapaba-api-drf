from django.utils.text import slugify
from django.contrib.auth import get_user_model
from accounts.utils.folder_utils import EstablishmentFolderRenamer


class UniqueUsernameGenerator:
    """Gera usernames únicos com base em um nome."""

    @staticmethod
    def generate_unique_username(base_name: str) -> str:
        UserModel = get_user_model()
        username = slugify(base_name).replace("-", "_")
        original_username = username
        counter = 1

        while UserModel.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1
            if counter > 100:
                raise ValueError("Não foi possível gerar um username único.")

        return username


class UsernameUtils:
    """Atualiza o username e renomeia as pastas vinculadas."""

    @staticmethod
    def update_rename_folder(instance, old_name: str, new_name: str):
        """Atualiza o username e renomeia pastas de mídia associadas."""
        if not new_name or new_name == old_name:
            return

        slugified_name = slugify(new_name).replace("-", "_")
        new_username = slugified_name

        UserModel = get_user_model()
        original_username = new_username
        counter = 1

        # Evita conflito de usernames
        while (
            UserModel.objects.filter(username=new_username)
            .exclude(pk=instance.user.pk)
            .exists()
        ):
            new_username = f"{original_username}_{counter}"
            counter += 1

        instance.user.username = new_username
        instance.user.save()

        EstablishmentFolderRenamer.rename_folders(
            instance.pk, old_username=old_name, new_username=new_username
        )
