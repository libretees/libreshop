import logging
from django.contrib import admin
from . import forms
from . import models

# Initialize logger
logger = logging.getLogger(__name__)

# Register your models here.
class LocationAdmin(admin.TabularInline):
    model = models.Location
    extra = 1


class AttributeAdmin(admin.TabularInline):
    model = models.Attribute_Value
    extra = 1


class InventoryAdmin(admin.ModelAdmin):
    form = forms.InventoryCreationForm
    inlines = [AttributeAdmin, LocationAdmin,]


admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.Location)
admin.site.register(models.Attribute)
admin.site.register(models.Attribute_Value)
admin.site.register(models.Warehouse)
