import logging
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

class Supply(TimeStampedModel):

    inventory = models.ForeignKey('Inventory', null=True, blank=True)
    purchase_order = models.ForeignKey(
        'PurchaseOrder',
        null=False,
        blank=False,
        related_name='supplies'
    )
    name = models.CharField(max_length=64, unique=True, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))])
    cost = models.DecimalField(max_digits=8, decimal_places=2,
        null=False, blank=False, default=Decimal('0.00'))
    landed_cost = models.DecimalField(max_digits=8, decimal_places=2,
        null=True, blank=True, default=Decimal('0.00'))
    receipt_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Supplies'
