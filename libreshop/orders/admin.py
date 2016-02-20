from django.contrib import admin
from django.db.models.aggregates import Count, Sum, IntegerField
from django.db.models.expressions import Case, When
from .models import Order, Purchase, TaxRate


class PurchaseInline(admin.TabularInline):

    model = Purchase
    fields = ('variant', 'price', 'fulfilled')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    date_hierarchy = 'created'
    inlines = (PurchaseInline,)
    list_display = (
        'token', '_recipient', '_purchases', '_fulfilled_purchases', 'subtotal',
        'sales_tax', 'shipping_cost', 'total', 'created', '_fulfilled'
    )


    def _fulfilled(self, instance):
        return instance.fulfilled_purchases == instance.purchase_count
    _fulfilled.boolean = True # Show Icon instead of 'True'/'False' text.


    def _fulfilled_purchases(self, instance):
        return instance.fulfilled_purchases
    _fulfilled_purchases.short_description = 'Fulfilled Purchases'
    _fulfilled_purchases.admin_order_field = 'fulfilled_purchases'


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
        queryset = queryset.annotate(
            purchase_count=Count('purchase'),
            fulfilled_purchases=Sum(
                Case(
                    When(purchase__fulfilled=True, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        return queryset


# Register your models here.
admin.site.register(Purchase)
admin.site.register(TaxRate)
