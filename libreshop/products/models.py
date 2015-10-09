import logging
from decimal import Decimal
from django.db import models
from django.db import transaction
from model_utils.models import TimeStampedModel
from jsonfield import JSONField


# Initialize logger.
logger = logging.getLogger(__name__)


# Create your models here.
class ProductManager(models.Manager):

    def create(self, *args, **kwargs):
        product = None
        with transaction.atomic():

            product = super(ProductManager, self).create(*args, **kwargs)
            variant_exists = bool(Variant.objects.filter(product=product))
            if not variant_exists:
                variant = Variant.objects.create(product=product)

        return product


class Product(TimeStampedModel):

    sku = models.CharField(max_length=8,
                           unique=True,
                           null=False)
    name = models.CharField(max_length=64,
                            unique=True,
                            null=False,
                            blank=False)

    objects = ProductManager()

    def save(self, *args, **kwargs):
        product = None
        with transaction.atomic():
            product = super(Product, self).save(*args, **kwargs)
            variant_exists = bool(Variant.objects.filter(product=self).count())
            if not variant_exists:
                variant = Variant.objects.create(product=self)

        return product

    def __str__(self):
        return self.name


class VariantManager(models.Manager):

    def create(self, *args, **kwargs):
        variant = None
        with transaction.atomic():
            variant = super(VariantManager, self).create(*args, **kwargs)
            component_exists = bool(Component.objects.filter(variant=variant).count())
            if not component_exists:
                component = Component.objects.create(variant=variant)

        return variant


class Variant(TimeStampedModel):

    product = models.ForeignKey(Product)
    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)
    sub_sku = models.CharField(max_length=8,
                               null=True,
                               blank=True)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                null=False,
                                default=Decimal('0.00'))

    objects = VariantManager()

    def save(self, *args, **kwargs):
        variant = None
        with transaction.atomic():
            variant = super(Variant, self).save(*args, **kwargs)

            component_exists = bool(Component.objects.filter(variant=self))

            if not component_exists:
                component = Component.objects.create(variant=self)

        return variant

    def delete(self, *args, **kwargs):
        super(Variant, self).delete(*args, **kwargs)

        product_exists = bool(Product.objects.get(id=self.product_id))
        variant_exists = bool(Variant.objects.filter(product=self.product))

        if product_exists and not variant_exists:
            variant = Variant.objects.create(product=self.product)

    def __str__(self):
        return self.name or 'Variant(%s) of Product: %s' % (self.id, self.product.sku)


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

    class Meta():
        verbose_name_plural = 'inventory'

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
    inventory = models.ForeignKey(Inventory,
                                  blank=True,
                                  null=True)
    quantity = models.DecimalField(max_digits=8,
                                   decimal_places=2,
                                   null=False,
                                   default=Decimal('1'))

    def __str__(self):
        return 'Component of Variant'
