from django.contrib import admin
from .models import Part, PartModel, PartStock, Assembly

admin.site.register(Part)
admin.site.register(PartModel)
admin.site.register(PartStock)
admin.site.register(Assembly)