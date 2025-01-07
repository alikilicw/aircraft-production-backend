from rest_framework import serializers
from .models import AircraftModel

class AircraftModelSeralizer(serializers.ModelSerializer):
    class Meta:
        model = AircraftModel
        fields = ['name']