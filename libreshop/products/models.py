import logging
from decimal import Decimal
from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError
from model_utils.models import TimeStampedModel
from inventory.models import Inventory

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class ProductManager(models.Manager):

    def create(self, *args, **kwargs):
        product = None
        with transaction.atomic():
            product = super(ProductManager, self).create(*args, **kwargs)

            variants = Variant.objects.filter(product=product)
            if not variants:
                variant = Variant.objects.create(product=product,
                    name=product.name)

        return product


class Product(TimeStampedModel):

    sku = models.CharField(max_length=8, unique=True, null=False, blank=False)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)

    objects = ProductManager()

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self._meta.get_field('sku').verbose_name = 'SKU'
        self._meta.get_field('sku').verbose_name_plural = 'SKUs'


    @property
    def salable(self):
        variants = self.variant_set.all()
        return any(variant.salable for variant in variants)


    def validate_unique(self, *args, **kwargs):
        super(Product, self).validate_unique(*args, **kwargs)

        sku_queryset = self.__class__._default_manager.filter(
            sku__iexact=self.sku
        )
        name_queryset = self.__class__._default_manager.filter(
            name__iexact=self.name
        )

        if not self._state.adding and self.pk:
            sku_queryset = sku_queryset.exclude(pk=self.pk)
            name_queryset = name_queryset.exclude(pk=self.pk)

        validation_errors = {}
        if sku_queryset.exists():
            validation_errors['sku'] = ['Product with this SKU already exists',]
        if name_queryset.exists():
            validation_errors['name'] = ['Product with this Name already exists',]

        if validation_errors:
            raise ValidationError(validation_errors)


    def save(self, *args, **kwargs):

        exclude = kwargs.pop('exclude', None)
        self.validate_unique(exclude)

        product = None
        with transaction.atomic():

            product = super(Product, self).save(*args, **kwargs)
            variants = Variant.objects.filter(product=self)

            if not variants:
                variant = Variant.objects.create(product=self,
                    name=self.name)

            if variants.count() == 1 and self.name != variants[0].name:
                variant = variants[0]
                variant.name = self.name
                variant.save(*args, **kwargs)

        return product

    def __str__(self):
        return self.name


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

    product = models.ForeignKey(Product, null=False, blank=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    sub_sku = models.CharField(max_length=8, null=True, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False,
        blank=False, default=Decimal('0.00'))
    enabled = models.BooleanField(default=True)

    objects = VariantManager()

    def __init__(self, *args, **kwargs):
        super(Variant, self).__init__(*args, **kwargs)
        self._meta.get_field('sub_sku').verbose_name = 'Sub-SKU'
        self._meta.get_field('sub_sku').verbose_name_plural = 'Sub-SKUs'


    @property
    def salable(self):
        components = self.component_set.all()
        return all(component.inventory for component in components)


    def validate_unique(self, *args, **kwargs):
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


class Component(TimeStampedModel):

    class Meta:
        unique_together = ('variant', 'inventory',)

    variant = models.ForeignKey(Variant, null=False, blank=False)
    inventory = models.ForeignKey(Inventory, blank=False, null=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, null=False,
        blank=False, default=Decimal('0.00'))

    def delete(self, *args, **kwargs):
        super(Component, self).delete(*args, **kwargs)

        variant = Variant.objects.get(id=self.variant_id)
        components = Component.objects.filter(variant=self.variant)

        if variant and not components:
            component = Component.objects.create(variant=self.variant)

    def __str__(self):
        return 'Component of %s' % self.variant.name
