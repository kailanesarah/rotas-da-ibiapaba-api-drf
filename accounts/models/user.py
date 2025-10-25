from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers.user_manager import CustomUserManager
from accounts.utils.id_utils import IDGenerator


def generate_user_id():
    return IDGenerator.generate("U")


class User(AbstractUser):
    """Modelo de usuário personalizado."""

    USER_TYPES = [
        ("establishment", "Establishment"),
        ("manager", "Manager"),
        ("admin", "Admin"),
    ]

    id = models.CharField(
        primary_key=True,
        default=generate_user_id,
        max_length=10,
        editable=False,
    )

    type = models.CharField(max_length=20, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    has_mfa = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.id} - {self.username}"
