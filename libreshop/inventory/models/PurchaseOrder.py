import logging
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (
    Case, Count, DecimalField, ExpressionWrapper, F, IntegerField, Sum, When)
from django.utils import timezone
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

class PurchaseOrderManager(models.Manager):
    def get_queryset(self):
        queryset = super(PurchaseOrderManager, self).get_queryset()
        queryset = queryset.annotate(
            subtotal=Sum('supplies__cost'),
            total=Sum('supplies__cost') + F('sales_tax') + F('shipping_cost'),
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

class PurchaseOrder(TimeStampedModel):

    number = models.CharField(verbose_name='Purchase Order (PO) Number',
        max_length=64, unique=True, null=False, blank=False)
    sales_tax = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal(0.00),
        validators=[MinValueValidator(Decimal('0.00'))])
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2,
        null=False, blank=False, default=Decimal('0.00'))
    submitted = models.DateTimeField(default=timezone.now)
    warehouse = models.ForeignKey('Warehouse', null=False, blank=False)

    objects = PurchaseOrderManager()

    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
