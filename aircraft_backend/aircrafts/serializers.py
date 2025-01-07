from rest_framework import serializers
from .models import AircraftModel
from django.apps import apps

# Serializer for the AircraftModel model
class AircraftModelSeralizer(serializers.ModelSerializer):
    class Meta:
        model = AircraftModel
        fields = ['id', 'name']

# Serializer for the Aircraft model
class AircraftSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) 
    model = AircraftModelSeralizer(read_only=True) 
    serial_number = serializers.UUIDField(read_only=True)
    production_completed = serializers.BooleanField(
        required=False, default=None
    )
    production_date = serializers.DateField(
        required=False, default=None
    )
    model_id = serializers.IntegerField(
        write_only=True, required=False
    )
    assembled_parts = serializers.SerializerMethodField()  # Custom field for fetching related parts

    # Method to get the assembled parts of the aircraft
    def get_assembled_parts(self, obj):
        from parts.serializers import PartSerializer  # Import locally to avoid circular dependecy

        # Dynamically get the Assembly model from the parts app
        Assembly = apps.get_model('parts', 'Assembly')
        assemblies = Assembly.objects.filter(aircraft=obj)

        # Extract parts from the assemblies
        parts = [assembly.part for assembly in assemblies]
        return PartSerializer(parts, many=True).data
