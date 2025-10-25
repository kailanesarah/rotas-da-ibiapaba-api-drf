from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Manager personalizado para o modelo de usuário."""

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
