import logging
from decimal import Decimal
from django.contrib import admin
from django.db.models import (
    Case, Count, DecimalField, ExpressionWrapper, F, IntegerField, Sum, When)
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
    exclude = ['landed_cost', 'units_received']
    min_num = 1
    extra = 0


@admin.register(models.PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [SupplyAdmin]
    list_display = (
        'number', 'submitted', '_subtotal', 'sales_tax', 'shipping_cost',
        '_total', '_status'
    )

    def _subtotal(self, instance):
        return instance.subtotal
    _subtotal.short_description = 'Subtotal'
    _subtotal.admin_order_field = 'subtotal'


    def _total(self, instance):
        return instance.total
    _total.short_description = 'Total'
    _total.admin_order_field = 'total_order_field'


    def _status(self, instance):
        status = None
        if instance.percent_received == 0:
            status = 'Open'
        elif instance.percent_received < 1:
            status = 'Partially Received'
        else:
            status = 'Closed'
        return status
    _status.short_description = 'Status'
    _status.admin_order_field = 'percent_received'

    def get_queryset(self, request):
        queryset = super(PurchaseOrderAdmin, self).get_queryset(request)
        queryset = queryset.annotate(
            subtotal=Sum('supplies__cost'),
            total_order_field=(
                Sum('supplies__cost') + F('sales_tax') + F('shipping_cost')),
            supplies_ordered=Count('supplies'),
            supplies_received=Sum(
                Case(
                    When(supplies__receipt_date__isnull=False, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        queryset = queryset.annotate(
            percent_received=ExpressionWrapper(
                Decimal('1.0')*F('supplies_received')/F('supplies_ordered'),
                output_field=DecimalField()
            )
        )

        return queryset


admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.Location)
admin.site.register(models.Supply, UnindexedAdmin)
admin.site.register(models.Warehouse)
