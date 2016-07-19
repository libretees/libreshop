import logging
from django.contrib import admin
from common.admin import UnindexedAdmin
from common.forms import UniqueTogetherFormSet
from .forms import SupplierCreationForm
from .models import (
    Carrier, FulfillmentOrder, FulfillmentPurchase, FulfillmentSetting,
    FulfillmentSettingValue, Shipment, Supplier
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
    model = FulfillmentSettingValue
    fields = ('setting', 'value')
    verbose_name = 'Fulfillment Setting'
    verbose_name_plural = 'Fulfillment Settings'
    formset = UniqueTogetherFormSet
    extra = 0


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    form = SupplierCreationForm


@admin.register(Shipment)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = (
        'token', 'carrier', 'tracking_id', 'shipping_cost'
    )


# Register your models here.
admin.site.register(Carrier)
admin.site.register(FulfillmentSetting, UnindexedAdmin)
