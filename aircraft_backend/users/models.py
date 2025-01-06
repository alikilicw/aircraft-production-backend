from django.contrib.auth.models import User
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.team.name}'