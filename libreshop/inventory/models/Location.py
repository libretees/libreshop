import logging
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

class Location(TimeStampedModel):

    class Meta:
        unique_together = ('inventory', 'warehouse')

    inventory = models.ForeignKey('Inventory', null=True, blank=True)
    warehouse = models.ForeignKey('Warehouse', null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )

    def __str__(self):
        return 'Warehouse %s: Location %s' % (self.warehouse.name, self.id)
