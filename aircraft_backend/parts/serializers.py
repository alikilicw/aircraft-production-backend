from rest_framework import serializers
from .models import Part, PartModel
from aircrafts.serializers import AircraftModelSeralizer

class PartModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    compatible_aircraft = AircraftModelSeralizer()

class PartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    serial_number = serializers.UUIDField(read_only=True)
    model = PartModelSerializer(read_only=True)
    is_assembled = serializers.BooleanField(read_only=True)

    model_id = serializers.IntegerField(write_only=True)

    def validate_model(self, value):
        from .models import PartModel
        if not PartModel.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid model ID.")
        return value

    # def create(self, validated_data):
    #     model_id = validated_data.pop('model_id')
    #     model_instance = PartModel.objects.get(id=model_id)
    #     part = Part.objects.create(model=model_instance, **validated_data)
    #     return part

    # def update(self, instance, validated_data):
    #     model_data = validated_data.get('model', None)
    #     if model_data:
    #         model_instance = PartModel.objects.get(id=model_data['id'])
    #         instance.model = model_instance
    #     instance.serial_number = validated_data.get('serial_number', instance.serial_number)
    #     instance.save()
    #     return instance