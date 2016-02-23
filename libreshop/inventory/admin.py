import logging
from django.contrib import admin
from common.forms import UniqueTogetherFormSet
from . import forms
from . import models

# Initialize logger
logger = logging.getLogger(__name__)


# Register your models here.
class LocationAdmin(admin.TabularInline):

    model = models.Location
    formset = UniqueTogetherFormSet
    min_num = 1
    extra = 0


class AttributeAdmin(admin.TabularInline):

    model = models.Attribute_Value
    extra = 0


class InventoryAdmin(admin.ModelAdmin):

    form = forms.InventoryCreationForm
    inlines = [AttributeAdmin, LocationAdmin]


admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.Location)
admin.site.register(models.Attribute)
admin.site.register(models.Warehouse)
