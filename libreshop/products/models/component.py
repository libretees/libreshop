import logging
from decimal import Decimal
from django.db import models
from django.db import transaction
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class ComponentManager(models.Manager):

    def create(self, *args, **kwargs):
        component = None
        with transaction.atomic():
            component = super(ComponentManager, self).create(*args, **kwargs)
            component.delete_invalid_components()

        return component


class Component(TimeStampedModel):

    class Meta:
        unique_together = ('variant', 'inventory',)

    variant = models.ForeignKey('products.Variant', null=False, blank=False)
    inventory = models.ForeignKey('inventory.Inventory', blank=False, null=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, null=False,
        blank=False, default=Decimal('0.00'))

    objects = ComponentManager()


    def delete_invalid_components(self):
        '''
        Do not permit valid and invalid Components to coexist.
        '''
        components = Component.objects.filter(variant=self.variant)
        invalid_components = Component.objects.filter(
            variant=self.variant, inventory=None)
        valid_components = [component for component in components
            if component not in invalid_components]
        if valid_components and invalid_components:
            invalid_components.delete()


    def save(self, *args, **kwargs):
        component = None
        with transaction.atomic():
            component = super(Component, self).save(*args, **kwargs)
            self.delete_invalid_components()

        return component


    def delete(self, *args, **kwargs):
        from .variant import Variant
        super(Component, self).delete(*args, **kwargs)

        variant = Variant.objects.get(id=self.variant_id)
        components = Component.objects.filter(variant=self.variant)

        if variant and not components:
            component = Component.objects.create(variant=self.variant)

    def __str__(self):
        return 'Component of %s' % self.variant.name
