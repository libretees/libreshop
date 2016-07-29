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
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        'token', '_recipient', 'carrier', 'tracking_id', '_weight',
        '_destination', 'shipping_cost')

    def _destination(self, instance):
        address = instance.order.shipping_address
        return '%s, %s, %s' % (address.locality, address.region, address.country)
    _destination.short_description = 'Destination'
    _destination.admin_order_field = 'order__shipping_address__locality'

    def _recipient(self, instance):
        address = instance.order.shipping_address
        return '%s' % address.recipient_name
    _recipient.short_description = 'Recipient'
    _recipient.admin_order_field = 'order__shipping_address__recipient_name'

    def _weight(self, instance):
        carrier_preferred_unit = instance.carrier.unit_of_measure
        return '%s %s' % (
            getattr(instance.weight, carrier_preferred_unit, 0),
            carrier_preferred_unit)
    _weight.short_description = 'Weight'
    _weight.admin_order_field = 'weight'


# Register your models here.
admin.site.register(Carrier)
admin.site.register(FulfillmentSetting, UnindexedAdmin)
