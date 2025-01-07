from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from .serializers import AircraftSerializer
from .models import AircraftModel, Aircraft

from users.permissions import IsPersonnel
from users.models import TeamSlugEnum


class AircraftAPIView(APIView):
    serializer_class = AircraftSerializer
    permission_classes = [IsPersonnel]

    def post(self, request):
        if request.team and request.team.slug != TeamSlugEnum.ASSEMBLY:
            raise ValidationError(
                f'You are not in the Assembly team.'
            )
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            aircraft_model = get_object_or_404(AircraftModel, id=serializer.validated_data['model_id'])

            aircraft = Aircraft.objects.create(model=aircraft_model)

            return Response(
                self.serializer_class(aircraft).data, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def get(self, request):
        aircrafts = Aircraft.objects.all()
        serializer = self.serializer_class(aircrafts, many=True)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
    

class AircraftDetailAPIView(APIView):
    serializer_class = AircraftSerializer
    permission_classes = [IsPersonnel]

    def get_object(self, pk):
        try:
            return Aircraft.objects.get(pk=pk)
        except Aircraft.DoesNotExist:
            return None

    def patch(self, request, pk):
        if request.team and request.team.slug != TeamSlugEnum.ASSEMBLY:
            return Response(
                f'You are not in the Assembly team.',
                status=status.HTTP_403_FORBIDDEN
            )

        aircraft = self.get_object(pk=pk)
        if aircraft is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        aircraft.production_completed = True
        aircraft.production_date = timezone.now().date()

        try:
            aircraft.clean()
            aircraft.save()
        except Exception as err:
            return Response(
                {'errors': err},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(aircraft)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )