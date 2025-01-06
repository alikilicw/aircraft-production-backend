from django.contrib.auth.models import AbstractUser
from django.db import models
from api.team.models import Team

class Personel(AbstractUser):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Personel'
        verbose_name_plural = 'Personels'