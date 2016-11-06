import logging
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.template.defaultfilters import slugify
from model_utils.models import TimeStampedModel
from versatileimagefield.fields import PPOIField, VersatileImageField
from .Image import Image
from .Variant import Variant

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class ProductManager(models.Manager):

    def create(self, *args, **kwargs):
        product = None
        with transaction.atomic():
            logger.info('Creating product...')
            product = super(ProductManager, self).create(*args, **kwargs)
            logger.info('Created product.')

            variants = Variant.objects.filter(product=product)
            if not variants:
                variant = Variant.objects.create(
                    product=product,
                    name=product.name
                )

        return product


class Product(TimeStampedModel):

    sku = models.CharField(max_length=8, unique=True, null=False, blank=False)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    description = models.CharField(max_length=2048, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    fulfillment_settings = models.ManyToManyField(
        'fulfillment.FulfillmentSetting',
        verbose_name='Default Fulfillment Settings',
        through='fulfillment.FulfillmentSettingValue',
        through_fields=('product', 'setting'),
        blank=True
    )

    objects = ProductManager()


    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self._meta.get_field('sku').verbose_name = 'SKU'
        self._meta.get_field('sku').verbose_name_plural = 'SKUs'


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


    @property
    def featured_image(self):
        image = Image.objects.filter(product=self, featured=True).latest()
        return image.file if image else None


    @property
    def images(self):
        images = Image.objects.filter(product=self, featured=False)
        return [image.file for image in images]


    @property
    def maximum_price(self):
        price = max([variant.price for variant in self.variants])
        return ('free' if price == 0.00 else ('$%s' % str(price)))


    @property
    def minimum_price(self):
        price = min([variant.price for variant in self.variants])
        return ('free' if price == 0.00 else ('$%s' % str(price)))


    @property
    def salable(self):
        return bool(self.variants)


    @property
    def variants(self):
        salable_variants = [
            variant for variant in self.variant_set.all() if variant.salable
        ]

        return sorted(salable_variants, key=lambda x: (x.price, x.created))


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

        # Fetch original data from the database.
        if self.pk:
            original_product = Product.objects.get(pk=self.pk)

        # Generate a slug, if one was not specified or if the name has changed.
        if not self.slug or self.name != original_product.name:
            # Generate slug.
            slug = slugify(self.name)
            available_slug = slug

            # Check whether the slug is available and regenerate if necessary.
            slug_used, iterations = (bool(Product.objects.filter(slug=slug)), 1)
            while slug_used:
                iterations += 1
                available_slug = slug + str(iterations)
                slug_used = bool(Product.objects.filter(slug=available_slug))

            self.slug = available_slug

        exclude = kwargs.pop('exclude', None)
        self.validate_unique(exclude)

        product = None
        with transaction.atomic():

            logger.info('Creating product...')
            product = super(Product, self).save(*args, **kwargs)
            logger.info('Created product.')

            variants = Variant.objects.filter(product=self)
            if not variants:
                variant = Variant.objects.create(product=self, name=self.name)

            if variants.count() == 1 and self.name != variants[0].name:
                variant = variants[0]
                variant.name = self.name
                variant.save(*args, **kwargs)

        return product


    def __str__(self):
        return self.name
