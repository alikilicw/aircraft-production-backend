from rest_framework.permissions import BasePermission
from .models import Personnel

class IsInTeam(BasePermission):
    """
    Allows access only to personnels who belong to a specific team.
    """

    def __init__(self, team_name):
        self.team_name = team_name

    def has_permission(self, request, view):
        try:
            # Get the personnel (team info is stored here)
            personnel = Personnel.objects.get(user=request.user)
        except Personnel.DoesNotExist:
            return False  # If no personnel exists, deny access

        # Check if the personnel's team matches the required team name
        return personnel.team.name == self.team_name
