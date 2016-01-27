import re
import logging
from decimal import Decimal
from operator import itemgetter
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from model_utils.models import TimeStampedModel
from .component import Component

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Manufacturer(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


class DropShipmentSetting(TimeStampedModel):

    class Meta:
        unique_together = ('manufacturer', 'name')

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)

    def __str__(self):
        return '%s: %s' % (self.manufacturer.name, self.name)


class DropShipmentSettingValue(TimeStampedModel):

    class Meta:
        verbose_name = 'drop shipment setting'
        verbose_name_plural = 'drop shipment settings'
        unique_together = ('setting', 'variant')

    setting = models.ForeignKey(
        'DropShipmentSetting', null=True, blank=True
    )
    variant = models.ForeignKey('Variant', null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)



class VariantManager(models.Manager):

    def create(self, *args, **kwargs):
        variant = None
        with transaction.atomic():
            variant = super(VariantManager, self).create(*args, **kwargs)

            components = Component.objects.filter(variant=variant)
            if not components:
                component = Component.objects.create(variant=variant)

        return variant


class Variant(TimeStampedModel):

    class Meta:
        unique_together = (
            ('product', 'name',),
            ('product', 'sub_sku',),
        )


    class Price(object):
        major_units = None
        minor_units = None

        def __init__(self, price):
            major_units, minor_units = itemgetter(0, 1)(str(price).split('.'))
            self.major_units = major_units
            self.minor_units = minor_units

        def __str__(self):
            return '.'.join([self.major_units, self.minor_units])


    product = models.ForeignKey('products.Product', null=False, blank=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    sub_sku = models.CharField(max_length=8, null=True, blank=False)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal('0.00'),
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    drop_shipment_settings = models.ManyToManyField(
        'DropShipmentSetting', through='DropShipmentSettingValue',
        through_fields=('variant', 'setting'), blank=True
    )
    enabled = models.BooleanField(default=True)

    objects = VariantManager()

    def __init__(self, *args, **kwargs):
        super(Variant, self).__init__(*args, **kwargs)
        self._meta.get_field('sub_sku').verbose_name = 'Sub-SKU'
        self._meta.get_field('sub_sku').verbose_name_plural = 'Sub-SKUs'


    @property
    def sku(self):
        return self.product.sku + self.sub_sku if self.sub_sku else ''


    @property
    def salable(self):
        components = self.component_set.all()
        return (False if not components else
            all(component.inventory for component in components))


    @property
    def attributes(self):

        numeric_pattern = r"""
            ^[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?$
        """
        regex = re.compile(numeric_pattern, re.VERBOSE)

        attributes = {}
        for component in self.component_set.all().order_by('-created'):
            for key in component.attributes:
                attribute = component.attributes[key]
                if key not in attributes:
                    attributes[key] = {attribute}
                else:
                    if re.match(regex, attribute):
                        for value in attributes[key]:
                            if re.match(regex, value):
                                try:
                                    augend = int(value)
                                except:
                                    augend = float(value)
                                try:
                                    addend = int(attribute)
                                except:
                                    addend = float(attribute)
                                attribute = str(augend + addend)
                                attributes[key].discard(value)
                                break
                    attributes[key].add(attribute)
        return attributes


    @property
    def split_price(self):
        return self.Price(self.price)


    def validate_unique(self, *args, **kwargs):
        from .product import Product
        super(Variant, self).validate_unique(*args, **kwargs)

        validation_errors = {}

        if self.sub_sku:
            sub_sku_queryset = self.__class__._default_manager.filter(
                product=self.product,
                sub_sku__iexact=self.sub_sku
            )
            if not self._state.adding and self.pk:
                sub_sku_queryset = sub_sku_queryset.exclude(pk=self.pk)
            if sub_sku_queryset.exists():
                validation_errors['sub_sku'] = ['Variant Sub-SKU for this Product already exists',]

            similar_skus = [
                product.sku + variant.sub_sku
                for product in Product.objects.filter(
                    sku__istartswith=self.product.sku[0]
                ).exclude(pk=self.product.pk)
                for variant in product.variant_set.filter(
                    sub_sku__iendswith=self.sub_sku[-1]
                )
            ]

            if self.sku in similar_skus:
                logger.error(
                    'Variant SKU is not unique. SKU \'%s\' found in [%s].' %
                    (self.sku, ', '.join(similar_skus))
                )
                validation_errors['sub_sku'] = ['Product SKU and Variant Sub-SKU are not unique at the catalog level',]

        if self.name:
            name_queryset = self.__class__._default_manager.filter(
                product=self.product,
                name__iexact=self.name
            )
            if not self._state.adding and self.pk:
                name_queryset = name_queryset.exclude(pk=self.pk)
            if name_queryset.exists():
                validation_errors['name'] = ['Variant Name for this Product already exists',]

        if validation_errors:
            raise ValidationError(validation_errors)


    def save(self, *args, **kwargs):

        exclude = kwargs.pop('exclude', None)
        self.validate_unique(exclude)

        variant = None
        with transaction.atomic():
            variant = super(Variant, self).save(*args, **kwargs)

            if (self.product.name != self.name and self.product.variant_set.
                count() == 1):
                self.name = self.product.name
                variant = self.save()

            components = Component.objects.filter(variant=self)

            if not components:
                component = Component.objects.create(variant=self)

        return variant

    def delete(self, *args, **kwargs):
        from .product import Product
        super(Variant, self).delete(*args, **kwargs)

        product = Product.objects.get(id=self.product_id)
        variants = Variant.objects.filter(product=self.product)

        if product and not variants:
            variant = Variant.objects.create(product=self.product)

        if (self.product.variant_set.count() == 1):
            variant = self.product.variant_set.first()
            variant.name = self.product.name
            variant.save(*args, **kwargs)

    def __str__(self):
        return self.name or 'Variant(%s) of Product: %s' % (self.id,
            self.product.sku)
