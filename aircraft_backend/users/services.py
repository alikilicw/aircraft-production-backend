from django.contrib.auth.models import User
from .models import Personnel

class UserService:
    def get_team(self, user: User):
        try:
            personnel = Personnel.objects.get(user=user.pk)
            return personnel.team
        except Personnel.DoesNotExist:
            return None