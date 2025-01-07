from rest_framework.permissions import BasePermission
from .services import UserService

class IsPersonnel(BasePermission):
    """
    Allows access only to personnels who belong to a specific team.
    """

    user_service = UserService()

    def has_permission(self, request, view):
        if request.user:
            team = self.user_service.get_team(request.user)
            if team:
                request.team = team
                return True

        return False
