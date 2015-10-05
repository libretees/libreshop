from django.db import models
from model_utils.models import TimeStampedModel
from jsonfield import JSONField

# Create your models here.
class Product(TimeStampedModel):
    sku = models.CharField(max_length=8,
                           null=True,
                           blank=True)

    def __str__(self):
        return self.name


class Variant(TimeStampedModel):

    product = models.ForeignKey(Product)
    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)
    sub_sku = models.CharField(max_length=8,
                               null=True,
                               blank=True)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2)

    def __str__(self):
        return self.name


class Location(TimeStampedModel):

    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)

    def __str__(self):
        return self.name


class Attribute(TimeStampedModel):

    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)


class Attribute_Value(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'attribute values'

    attribute = models.ForeignKey('Attribute')
    inventory = models.ForeignKey('Inventory')
    value = models.CharField(max_length=64,
                             null=True,
                             blank=True)


class Inventory(TimeStampedModel):

    location = models.ForeignKey(Location)
    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)
    attributes = models.ManyToManyField(Attribute,
                                        through='Attribute_Value',
                                        through_fields=('inventory', 'attribute'))
    alternatives = models.ManyToManyField('self')
    quantity = models.DecimalField(max_digits=8,
                                   decimal_places=2)
    cost = models.DecimalField(max_digits=8,
                               decimal_places=2)

    def __str__(self):
        return self.name


class Component(TimeStampedModel):

    variant = models.ForeignKey(Variant)
    inventory = models.ForeignKey(Inventory)
    quantity = models.DecimalField(max_digits=8,
                                   decimal_places=2)

    def __str__(self):
        return self.name
