from django.contrib import admin
from django.db.models import Count
from .models import Order, Purchase, TaxRate


class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'token', '_recipient', '_purchases', 'subtotal', 'sales_tax',
        'shipping_cost', 'total', 'created'
    )

    def _purchases(self, instance):
        return instance.purchase_count
    _purchases.short_description = 'Purchases'
    _purchases.admin_order_field = 'purchase_count'


    def _recipient(self, instance):
        return instance.shipping_address.recipient_name
    _recipient.short_description = 'Recipient'
    _recipient.admin_order_field = 'shipping_address__recipient_name'


    def get_queryset(self, request):
        queryset = super(OrderAdmin, self).get_queryset(request)
        queryset = queryset.annotate(purchase_count=Count('purchase'))
        return queryset


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(Purchase)
admin.site.register(TaxRate)
