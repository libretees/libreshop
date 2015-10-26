import logging
from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
from model_utils.models import TimeStampedModel
from .variant import Variant

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
        return (False if not variants else
            any(variant.salable for variant in variants))


    @property
    def attributes(self):

        attributes = {}
        variants = self.variant_set.all().order_by('created')
        for variant in variants:
            for key in variant.attributes:
                variant_attributes = variant.attributes[key]
                if key not in attributes:
                    attributes[key] = list(variant_attributes)
                else:
                    for attribute in variant_attributes:
                        if attribute not in attributes[key]:
                            attributes[key].append(attribute)

        return attributes


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
