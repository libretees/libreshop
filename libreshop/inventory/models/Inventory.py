import logging
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django_measurement.models import MeasurementField
from model_utils.models import TimeStampedModel
from measurement.measures import Weight
from orders.models import Purchase
from .Supply import Supply

# Initialize logger.
logger = logging.getLogger(__name__)

class Inventory(TimeStampedModel):

    name = models.CharField(max_length=64, null=False, blank=False)
    warehouses = models.ManyToManyField(
        'Warehouse', through='Location',
        through_fields=('inventory', 'warehouse'), blank=True
    )
    alternatives = models.ManyToManyField('self', blank=True)
    weight = MeasurementField(
        measurement=Weight, blank=False, null=False,
        default=Decimal(0.00),
        validators=[MinValueValidator(Decimal('0.00'))],
        unit_choices=(
            ('g', 'g'),
            ('kg', 'kg'),
            ('oz', 'oz'),
            ('lb', 'lb')
        )
    )
    packed_weight = MeasurementField(
        verbose_name='Packed Weight',
        measurement=Weight, blank=False, null=False,
        default=Decimal(0.00),
        validators=[MinValueValidator(Decimal('0.00'))],
        unit_choices=(
            ('g', 'g'),
            ('kg', 'kg'),
            ('oz', 'oz'),
            ('lb', 'lb')
        )
    )
    conversion_factor = models.DecimalField(
        verbose_name='Purchasing Conversion Factor',
        max_digits=8, decimal_places=2, default=Decimal(1.00),
        validators=[MinValueValidator(Decimal('0.00'))]
    )


    @property
    def fifo_cost(self):
        """
        Return the current inventory cost, using the FIFO accounting method.
        """
        return self.get_fifo_cost()


    def get_fifo_cost(self, for_date=None):
        """
        Return the inventory cost for a specific date, using the FIFO accounting
        method.

        :type for_date: datetime
        :param for_date: The date and time for which an inventory cost is
            needed.
        """
        # If a date was not specified, assume that the current cost is needed.
        if not for_date:
            for_date = timezone.now()

        logger.info('Getting FIFO cost for "%s" %s...' %
            (self.name, for_date.strftime('%Y-%m-%d %H:%M:%S')))

        # Determine the amount of inventory needed up to the date specified.
        inventory_needed = sum(
            component.quantity for purchase
            in Purchase.objects.filter(created__lte=for_date)
            for component in purchase.variant.components.filter(inventory=self))

        logger.debug('%d units of %s are needed for this date.' % (
            inventory_needed, self.name))

        # Determine the amount of supplies received up to the date specified.
        supplies_received = [
            supply for supply
            in Supply.objects.filter(inventory=self,
            receipt_date__lte=for_date).order_by('receipt_date')]

        logger.debug('%i supply shipments have been received by this date.' % (
            len(supplies_received)))

        # Determine which Supply the Inventory originates from.
        fifo_cost = Decimal(0.00)
        for supply in supplies_received:
            inventory_needed -= supply.units_received
            fifo_cost = supply.unit_cost
            if inventory_needed < 0:
                break
        logger.info('The FIFO cost for "%s" is %s.' % (self.name, fifo_cost))

        return fifo_cost


    def delete(self, *args, **kwargs):
        from products.models import Component

        linked_components = Component.objects.filter(inventory=self)
        for component in linked_components:
            component.inventory = None
            component.save()

        super(Inventory, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'inventory'
