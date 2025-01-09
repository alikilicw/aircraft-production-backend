from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Personnel
from .serializers import PersonnelSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .permissions import IsPersonnel

class WhoAmIView(APIView):
    permission_classes = [IsPersonnel]

    def get(self, request):
        personnel = get_object_or_404(Personnel, user=request.user)
        serializer = PersonnelSerializer(personnel)
        return Response(serializer.data)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response("Successfully logged out.", status=200)
        except Token.DoesNotExist:
            return Response("Invalid token or already logged out.", status=400)

