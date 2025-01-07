from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Part
from .serializers import PartSerializer
from users.services import UserService
from users.permissions import IsPersonnel
from .models import PartModel
from rest_framework.exceptions import ValidationError

class PartAPIView(APIView):
    serializer_class = PartSerializer
    permission_classes = [IsPersonnel]

    def get(self, request):
        parts = Part.objects.all()
        if request.team:
            team_models = PartModel.objects.filter(team=request.team)
            parts = parts.filter(model__in=team_models)


        serial_number = request.query_params.get('serial_number', None)
        model_id = request.query_params.get('model', None)

        if serial_number:
            parts = parts.filter(serial_number=serial_number)
        
        if model_id:
            parts = parts.filter(model_id=model_id)

        serializer = self.serializer_class(parts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.team:
                try:
                    model_instance = PartModel.objects.get(
                        id=serializer.validated_data['model_id'])
                except PartModel.DoesNotExist:
                    return Response(
                        {'error': 'Model not found.'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                if model_instance.team == request.team:
                    part = Part.objects.create(model=model_instance)
                else:
                    raise ValidationError(f'You are not in {model_instance.team.name}.')

                return Response(
                    self.serializer_class(part).data, 
                    status=status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST)

class PartDetailAPIView(APIView):
    serializer_class = PartSerializer
    permission_classes = [IsPersonnel]

    def get_object(self, pk):
        try:
            return Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return None

    def get(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.team:
            if part.model.team != request.team:
                return Response(
                    f'You are not in {part.model.team.name}.',
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.serializer_class(part)
        return Response(serializer.data)

    def delete(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.team:
            if part.model.team != request.team:
                return Response(
                    f'You are not in {part.model.team.name}.',
                    status=status.HTTP_403_FORBIDDEN
                )

        part.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)