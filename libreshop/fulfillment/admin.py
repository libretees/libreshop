import logging
from django.contrib import admin
from common.admin import UnindexedAdmin
from common.forms import UniqueTogetherFormSet
from .forms import SupplierCreationForm
from .models import (
    FulfillmentOrder, FulfillmentPurchase, FulfillmentSetting,
    FulfillmentSettingValue, Supplier
)

# Initialize logger
logger = logging.getLogger(__name__)

class FulfillmentPurchaseInline(admin.TabularInline):

    model = FulfillmentPurchase
    fields = ('purchase', 'subtotal', 'shipping_cost', 'tax', 'fees', 'total')
    readonly_fields = fields
    can_delete = False
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        return FulfillmentPurchase.objects.filter(order=obj).count()


@admin.register(FulfillmentOrder)
class FulfillmentOrderAdmin(admin.ModelAdmin):

    list_display = (
        'order_id', 'subtotal', 'shipping_cost', 'tax', 'fees', 'total',
        'created_at'
    )
    readonly_fields = list_display
    inlines = [FulfillmentPurchaseInline]


class FulfillmentSettingValueInline(admin.TabularInline):
    fields = ('setting', 'value')
    model = FulfillmentSettingValue
    formset = UniqueTogetherFormSet
    extra = 0


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    form = SupplierCreationForm


# Register your models here.
admin.site.register(FulfillmentSetting, UnindexedAdmin)
