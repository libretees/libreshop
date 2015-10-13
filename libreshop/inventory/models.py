import logging
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Warehouse(TimeStampedModel):

    name = models.CharField(max_length=64, null=True, blank=True)
    address = models.ForeignKey('shop.Address')

    def __str__(self):
        return 'Warehouse %s' % self.name


class Attribute(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


class Attribute_Value(TimeStampedModel):

    class Meta():
        verbose_name = 'attribute'
        verbose_name_plural = 'attributes'

    attribute = models.ForeignKey('Attribute')
    inventory = models.ForeignKey('Inventory')
    value = models.CharField(max_length=64, null=True, blank=True)


class Location(TimeStampedModel):

    inventory = models.ForeignKey('Inventory')
    warehouse = models.ForeignKey('Warehouse')
    quantity = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return '%s: Location %s' % (self.warehouse.name, self.id)


class Inventory(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'inventory'

    name = models.CharField(max_length=64, null=False, blank=False)
    warehouses = models.ManyToManyField('Warehouse', through='Location',
        through_fields=('inventory', 'warehouse'))
    attributes = models.ManyToManyField('Attribute', through='Attribute_Value',
        through_fields=('inventory', 'attribute'))
    alternatives = models.ManyToManyField('self', blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2,
        default=Decimal(0.00), validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return self.name
