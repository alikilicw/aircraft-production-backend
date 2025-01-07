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


# API view for managing aircrafts
class AircraftAPIView(APIView):
    serializer_class = AircraftSerializer
    permission_classes = [IsPersonnel]  # Ensure only personnel with proper permissions can access

    # Handle POST requests to create a new aircraft
    def post(self, request):
        # Check if the user's team is the Assembly team
        if request.team and request.team.slug != TeamSlugEnum.ASSEMBLY:
            raise ValidationError(
                f'You are not in the Assembly team.'
            )
        
        serializer = self.serializer_class(data=request.data)

        # Validate the request data
        if serializer.is_valid():
            # Ensure the provided model ID corresponds to an existing AircraftModel
            aircraft_model = get_object_or_404(
                AircraftModel, id=serializer.validated_data['model_id']
            )

            # Create a new aircraft with the provided model
            aircraft = Aircraft.objects.create(model=aircraft_model)

            return Response(
                self.serializer_class(aircraft).data, 
                status=status.HTTP_201_CREATED  # Return 201 Created on success
            )
        
        # Return validation errors if the input data is invalid
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Handle GET requests to retrieve all aircrafts
    def get(self, request):
        aircrafts = Aircraft.objects.all()  # Fetch all aircraft records
        serializer = self.serializer_class(aircrafts, many=True)  # Serialize the data
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK  # Return 200 OK on success
        )
    

# API view for managing a specific aircraft
class AircraftDetailAPIView(APIView):
    serializer_class = AircraftSerializer
    permission_classes = [IsPersonnel]  # Ensure only personnel with proper permissions can access

    # Helper method to fetch a specific aircraft by primary key
    def get_object(self, pk):
        try:
            return Aircraft.objects.get(pk=pk)
        except Aircraft.DoesNotExist:
            return None

    # Handle PATCH requests to update the production status of an aircraft
    def patch(self, request, pk):
        # Check if the user's team is the Assembly team
        if request.team \
            and request.team.slug != TeamSlugEnum.ASSEMBLY:
            return Response(
                f'You are not in the Assembly team.',
                status=status.HTTP_403_FORBIDDEN  # Return 403 Forbidden if unauthorized
            )

        # Fetch the aircraft instance
        aircraft = self.get_object(pk=pk)
        if aircraft is None:
            return Response(status=status.HTTP_404_NOT_FOUND)  # Return 404 Not Found if the aircraft doesn't exist
        
        # Update the production status and production date
        aircraft.production_completed = True
        aircraft.production_date = timezone.now().date()

        # Attempt to clean and save the updated aircraft instance
        try:
            aircraft.clean()
            aircraft.save()
        except Exception as err:
            return Response(
                {'errors': err},  # Return validation errors if saving fails
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(aircraft)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK  # Return 200 OK on success
        )
