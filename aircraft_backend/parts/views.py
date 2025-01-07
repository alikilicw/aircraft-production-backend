from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from .models import Part, PartStock, PartModel, Assembly
from .serializers import PartSerializer, AssemblySerializer

from aircrafts.models import Aircraft

from users.permissions import IsPersonnel
from users.models import TeamSlugEnum


class PartAPIView(APIView):
    serializer_class = PartSerializer
    permission_classes = [IsPersonnel]

    def get(self, request):
        # Filter parts based on team and query parameters
        parts = Part.objects.filter(in_stock=True)
        if request.team \
            and request.team.slug != TeamSlugEnum.ASSEMBLY:
            team_model = get_object_or_404(PartModel, team=request.team)
            parts = parts.filter(model=team_model)

        serial_number = request.query_params.get('serial_number', None)
        model_id = request.query_params.get('model', None)

        if serial_number:
            parts = parts.filter(serial_number=serial_number)
        if model_id:
            parts = parts.filter(model_id=model_id)

        serializer = self.serializer_class(parts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a part if the request is valid
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.team:
                model_instance = get_object_or_404(
                    PartModel, id=serializer.validated_data['model_id']
                )
                if model_instance.team != request.team:
                    raise ValidationError(
                        f'You are not in the {model_instance.team.name}.'
                    )

                part = Part.objects.create(model=model_instance)
                part_stock = get_object_or_404(
                    PartStock, part_model=part.model
                )

                part_stock.stock += 1
                part_stock.save()

                return Response(
                    self.serializer_class(part).data, 
                    status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class PartDetailAPIView(APIView):
    serializer_class = PartSerializer
    permission_classes = [IsPersonnel]

    def get_object(self, pk):
        # Fetch a part by primary key
        return Part.objects.filter(pk=pk).first()

    def get(self, request, pk):
        # Return part details
        part = self.get_object(pk)
        if not part:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.team and part.model.team != request.team:
            return Response(
                f'You are not in the {part.model.team.name}.',
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.serializer_class(part)
        return Response(serializer.data)

    def delete(self, request, pk):
        # Delete a part and update stock
        part = self.get_object(pk)
        if not part:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.team and part.model.team != request.team:
            return Response(
                f'You are not in the {part.model.team.name}.',
                status=status.HTTP_403_FORBIDDEN
            )

        part_stock = get_object_or_404(PartStock, part_model=part.model)
        if part.in_stock:
            part_stock.stock -= 1
            part_stock.save()
        part.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssemblyAPIView(APIView):
    serializer_class = AssemblySerializer
    permission_classes = [IsPersonnel]

    def post(self, request):
        # Create an assembly
        if request.team and request.team.slug != TeamSlugEnum.ASSEMBLY:
            raise ValidationError(
                f'You are not in the Assembly team.'
            )

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            aircraft = get_object_or_404(
                Aircraft, id=serializer.validated_data['aircraft_id']
            )
            part = get_object_or_404(
                Part, id=serializer.validated_data['part_id']
            )

            if not part.in_stock:
                raise ValidationError(
                    'The part was already used.'
                )
            if part.model.compatible_aircraft != aircraft.model:
                raise ValidationError(
                    'The part is incompatible with the aircraft.'
                )
            if Assembly.objects.filter(
                aircraft=aircraft, part__model=part.model
            ).exists():
                raise ValidationError(
                    'This aircraft already has that part.'
                )

            with transaction.atomic():
                assembly = Assembly.objects.create(aircraft=aircraft, part=part)
                part.in_stock = False
                part.save()

                part_stock = get_object_or_404(
                    PartStock, part_model=part.model
                )
                part_stock.stock -= 1
                part_stock.save()

            return Response(
                self.serializer_class(assembly).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        # Return all assemblies
        if request.team \
            and request.team.slug != TeamSlugEnum.ASSEMBLY:
            raise ValidationError(
                f'You are not in the Assembly team.'
            )

        assemblies = Assembly.objects.all()
        serializer = self.serializer_class(assemblies, many=True)
        return Response(serializer.data)
