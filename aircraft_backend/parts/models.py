import uuid
from django.db import models
from aircrafts.models import AircraftModel, Aircraft
from users.models import Team

class PartModel(models.Model):
    MODEL_CHOICES = [
        ('wing', 'Wing'),
        ('fuselage', 'Fuselage'),
        ('tail', 'Tail'),
        ('avionics', 'Avionics'),
    ]

    name = models.CharField(max_length=8, choices=MODEL_CHOICES)
    compatible_aircraft = models.ForeignKey(AircraftModel, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.compatible_aircraft.name}'

class Part(models.Model):
    serial_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    model = models.ForeignKey(PartModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.model.name} - {self.model.compatible_aircraft} - {self.serial_number}'
    
class PartStock(models.Model):
    part_model = models.ForeignKey(PartModel, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.part_model.name} - {self.part_model.compatible_aircraft.name}: {self.stock}"
    

class Assembly(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.DO_NOTHING, related_name='assemblies')
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING, related_name='assemblies')

    def __str__(self):
        return f"{self.aircraft.model.name} - {self.part.model.name}"
