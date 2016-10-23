import logging
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django_measurement.models import MeasurementField
from model_utils.models import TimeStampedModel
from measurement.measures import Weight

# Initialize logger.
logger = logging.getLogger(__name__)

class Inventory(TimeStampedModel):

    name = models.CharField(max_length=64, null=False, blank=False)
    warehouses = models.ManyToManyField(
        'Warehouse', through='Location',
        through_fields=('inventory', 'warehouse'), blank=True
    )
    alternatives = models.ManyToManyField('self', blank=True)
    cost = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal(0.00),
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    weight = MeasurementField(
        measurement=Weight, blank=False, null=False,
        unit_choices=(
            ('g', 'g'),
            ('kg', 'kg'),
            ('oz', 'oz'),
            ('lb', 'lb')
        )
    )
    packed_weight = MeasurementField(
        verbose_name='Packed Weight',
        measurement=Weight, blank=False, null=False,
        unit_choices=(
            ('g', 'g'),
            ('kg', 'kg'),
            ('oz', 'oz'),
            ('lb', 'lb')
        )
    )
    conversion_factor = models.DecimalField(
        verbose_name='Purchasing Conversion Factor',
        max_digits=8, decimal_places=2, default=Decimal(1.00),
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def delete(self, *args, **kwargs):
        from products.models import Component

        linked_components = Component.objects.filter(inventory=self)
        for component in linked_components:
            component.inventory = None
            component.save()

        super(Inventory, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'inventory'
