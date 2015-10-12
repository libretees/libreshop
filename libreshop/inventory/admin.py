from . import models
from django.contrib import admin

# Register your models here.
admin.site.register(models.Inventory)
admin.site.register(models.InventoryLocation)
admin.site.register(models.Attribute)
admin.site.register(models.Attribute_Value)