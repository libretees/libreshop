import logging
from django.contrib import admin
from contrib.admin import UnindexedAdmin
from contrib.forms import UniqueTogetherFormSet
from .forms import ManufacturerCreationForm
from .models import DropShipmentSetting, DropShipmentSettingValue, Manufacturer

# Initialize logger
logger = logging.getLogger(__name__)

# Register your models here.
class DropShipmentSettingValueInline(admin.TabularInline):

    model = DropShipmentSettingValue
    formset = UniqueTogetherFormSet
    extra = 0


class ManufacturerAdmin(admin.ModelAdmin):

    form = ManufacturerCreationForm


admin.site.register(DropShipmentSetting, UnindexedAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
