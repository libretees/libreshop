import logging
from django.contrib import admin
from common.admin import UnindexedAdmin
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


class InventoryAdmin(admin.ModelAdmin):
    form = forms.InventoryCreationForm
    inlines = [LocationAdmin]


class SupplyAdmin(admin.TabularInline):
    model = models.Supply
    min_num = 1
    extra = 0

@admin.register(models.PurchaseOrder)
class PurchaseOrder(admin.ModelAdmin):
    inlines = [SupplyAdmin]


admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.Location)
admin.site.register(models.Supply, UnindexedAdmin)
admin.site.register(models.Warehouse)
