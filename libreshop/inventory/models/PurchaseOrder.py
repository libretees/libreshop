import logging
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

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

    @property
    def weight(self):
        return sum(supply.weight for supply in self.supplies.all())

    @property
    def total(self):
        calculated_total = (
            sum(supply.cost for supply in self.supplies.all()) +
            self.sales_tax +
            self.shipping_cost)
        return calculated_total

    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
