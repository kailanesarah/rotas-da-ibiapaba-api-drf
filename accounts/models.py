from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from categories.models import Category

STATE_CHOICES = (
    ("CE", "Ceará"),
    ("PI", "Piauí"),
    ("MA", "Maranhão"),
    ("BA", "Bahia"),
)


class Location(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES, max_length=3)
    city = models.CharField(max_length=100)
    CEP = models.CharField(max_length=8)
    neighborhood = models.CharField(max_length=60)
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    complement = models.CharField(blank=True, null=True, max_length=250)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório")

        if self.model.objects.filter(username=username).exists():
            raise ValueError("Esse usuário já existe")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError("A senha é obrigatória")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    TYPES_USER = [
        ("establishment", "establishment"),
        ("manager", "manager"),
        ("admin", "admin"),
    ]

    type = models.CharField(max_length=20, choices=TYPES_USER)
    email = models.EmailField(unique=True)
    has_mfa = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Establishment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="establishment_user"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    CNPJ = models.CharField(max_length=14)
    whatsapp = models.BigIntegerField()  # para números maiores que IntegerField
    # social_media = models.ForeignKey(
    #     SocialMedia, on_delete=models.CASCADE, related_name="establishment_social_media"
    # )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="establishment_location"
    )
    category = models.ManyToManyField(Category, related_name="establishments_category")


# class SocialMedia:
#     pass
