import logging
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)


class Warehouse(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    address = models.OneToOneField('addresses.Address', null=False, blank=False)


    def __str__(self):
        return 'Warehouse %s' % self.name


    def validate_unique(self, *args, **kwargs):
        super(Warehouse, self).validate_unique(*args, **kwargs)

        queryset = self.__class__._default_manager.filter(
            name__iexact=self.name
        )

        if not self._state.adding and self.pk:
            queryset = queryset.exclude(pk=self.pk)

        if queryset.exists():
            raise ValidationError({
                'name': ['Warehouse with this Name already exists',],
            })


    def save(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)
        self.validate_unique(exclude)
        super(Warehouse, self).save(*args, **kwargs)


class Location(TimeStampedModel):

    class Meta:
        unique_together = ('inventory', 'warehouse')


    inventory = models.ForeignKey('Inventory', null=True, blank=True)
    warehouse = models.ForeignKey('Warehouse', null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )


    def __str__(self):
        return 'Warehouse %s: Location %s' % (self.warehouse.name, self.id)


class Inventory(TimeStampedModel):

    class Meta:
        verbose_name_plural = 'inventory'


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


    def delete(self, *args, **kwargs):
        from products.models import Component

        linked_components = Component.objects.filter(inventory=self)
        for component in linked_components:
            component.inventory = None
            component.save()

        super(Inventory, self).delete(*args, **kwargs)


    def __str__(self):
        return self.name
