import logging
from django.contrib import admin
from common.admin import UnindexedAdmin
from common.forms import UniqueTogetherFormSet
from .forms import SupplierCreationForm
from .models import FulfillmentSetting, FulfillmentSettingValue, Supplier

# Initialize logger
logger = logging.getLogger(__name__)

# Register your models here.
class FulfillmentSettingValueInline(admin.TabularInline):

    model = FulfillmentSettingValue
    formset = UniqueTogetherFormSet
    extra = 0


class SupplierAdmin(admin.ModelAdmin):

    form = SupplierCreationForm


admin.site.register(FulfillmentSetting, UnindexedAdmin)
admin.site.register(Supplier, SupplierAdmin)
