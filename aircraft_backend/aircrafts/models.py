import uuid
from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError

class AircraftModel(models.Model):
    MODEL_CHOICES = [
        ('tb2', 'TB2'),
        ('tb3', 'TB3'),
        ('akinci', 'Akinci'),
        ('kizilelma', 'Kizilelma'),
    ]

    name = models.CharField(max_length=9, choices=MODEL_CHOICES, unique=True)

    def __str__(self):
        return self.name


class Aircraft(models.Model):
    model = models.ForeignKey(AircraftModel, on_delete=models.CASCADE)
    serial_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    production_completed = models.BooleanField(default=False)
    production_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.model.name} - {self.serial_number}'
    
    # Custom validation method for the Aircraft model's production completed mechanism
    def clean(self):
        # Validation only applies if production is marked as completed
        if self.production_completed:
            assemblies = self.assemblies.all()
            PartModel = apps.get_model('parts', 'PartModel')

            # Get all part models compatible with this aircraft's model
            part_models = PartModel.objects.filter(compatible_aircraft=self.model)

            # Ensure an aircraft has all parts required
            for model in part_models:
                if not assemblies.filter(part__model=model).exists():
                    raise ValidationError(f"Assembly of {model.name} is missing.")