from django.db import models

STATE_CHOICES = (
    ("CE", "Ceará"),
    ("PI", "Piauí"),
    ("MA", "Maranhão"),
    ("BA", "Bahia"),
)


class Location(models.Model):
    """Endereço do estabelecimento."""

    country = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES, max_length=3)
    city = models.CharField(max_length=100)
    CEP = models.CharField(max_length=8)
    neighborhood = models.CharField(max_length=60)
    street = models.CharField(max_length=100)
    number = models.IntegerField(null=True)
    complement = models.CharField(blank=True, null=True, max_length=250)

    def __str__(self):
        return f"{self.city}/{self.state}"
