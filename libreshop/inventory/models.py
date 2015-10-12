import logging
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Warehouse(TimeStampedModel):

    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)
    address = models.ForeignKey('shop.Address')


class Attribute(TimeStampedModel):

    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)


class Attribute_Value(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'attribute values'

    attribute = models.ForeignKey(Attribute)
    inventory = models.ForeignKey('Inventory')
    value = models.CharField(max_length=64,
                             null=True,
                             blank=True)


class Location(TimeStampedModel):

    warehouse = models.ForeignKey(Warehouse)
    quantity = models.DecimalField(max_digits=8,
                                   decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'inventory'

    location = models.ForeignKey(Location)

    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)
    attributes = models.ManyToManyField(Attribute,
                                        through=Attribute_Value,
                                        through_fields=('inventory', 'attribute'))
    alternatives = models.ManyToManyField('self')
    cost = models.DecimalField(max_digits=8,
                               decimal_places=2)

    def __str__(self):
        return self.name
