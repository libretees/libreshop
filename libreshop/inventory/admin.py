from . import models
from django.contrib import admin

# Register your models here.
admin.site.register(models.Inventory)
admin.site.register(models.Location)
admin.site.register(models.Attribute)
admin.site.register(models.Attribute_Value)
admin.site.register(models.Warehouse)
