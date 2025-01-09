from rest_framework import serializers
from .models import PartModel, PartStock
from aircrafts.serializers import AircraftModelSeralizer, AircraftSerializer

# Serializer for PartModel
class PartModelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    compatible_aircraft = AircraftModelSeralizer()
    stock = serializers.SerializerMethodField()

    def get_stock(self, obj):
        # get stock from PartStock
        try:
            part_stock = PartStock.objects.get(part_model=obj)
            return part_stock.stock
        except PartStock.DoesNotExist:
            return 0


# Serializer for Part
class PartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    serial_number = serializers.UUIDField(read_only=True)
    model = PartModelSerializer(read_only=True)
    is_assembled = serializers.BooleanField(read_only=True)

    model_id = serializers.IntegerField(write_only=True)

    def validate_model(self, value):
        if not PartModel.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid model ID.")
        return value

# Serializer for Assembly
class AssemblySerializer(serializers.Serializer):
    aircraft = AircraftSerializer(read_only=True) 
    part = PartSerializer(read_only=True)

    aircraft_id = serializers.IntegerField(write_only=True)
    part_id = serializers.IntegerField(write_only=True)
