import logging
from django.contrib import admin
from contrib.admin import UnindexedAdmin
from contrib.forms import UniqueTogetherFormSet
from .forms import SupplierCreationForm
from .models import DropShipmentSetting, DropShipmentSettingValue, Supplier

# Initialize logger
logger = logging.getLogger(__name__)

# Register your models here.
class DropShipmentSettingValueInline(admin.TabularInline):

    model = DropShipmentSettingValue
    formset = UniqueTogetherFormSet
    extra = 0


class SupplierAdmin(admin.ModelAdmin):

    form = SupplierCreationForm


admin.site.register(DropShipmentSetting, UnindexedAdmin)
admin.site.register(Supplier, SupplierAdmin)
