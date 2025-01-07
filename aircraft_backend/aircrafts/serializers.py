from rest_framework import serializers
from .models import AircraftModel
from django.apps import apps

class AircraftModelSeralizer(serializers.ModelSerializer):
    class Meta:
        model = AircraftModel
        fields = ['id', 'name']

class AircraftSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    model = AircraftModelSeralizer(read_only=True)
    serial_number = serializers.UUIDField(read_only=True)
    production_completed = serializers.BooleanField(required=False, default=None)
    production_date = serializers.DateField(required=False, default=None)
    model_id = serializers.IntegerField(write_only=True, required=False)
    assembled_parts = serializers.SerializerMethodField()

    def get_assembled_parts(self, obj):
        from parts.serializers import PartSerializer

        Assembly = apps.get_model('parts', 'Assembly')
        assemblies = Assembly.objects.filter(aircraft=obj)

        parts = [assembly.part for assembly in assemblies]
        return PartSerializer(parts, many=True).data