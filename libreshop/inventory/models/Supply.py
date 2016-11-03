import logging
from decimal import Decimal, InvalidOperation
from django.core.validators import MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

class Supply(TimeStampedModel):

    inventory = models.ForeignKey('Inventory', null=True, blank=True)
    purchase_order = models.ForeignKey(
        'PurchaseOrder',
        null=False,
        blank=False,
        related_name='supplies'
    )
    name = models.CharField(max_length=64, unique=True, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal('0.00'))])
    cost = models.DecimalField(max_digits=8, decimal_places=2,
        null=False, blank=False, default=Decimal('0.00'))
    landed_cost = models.DecimalField(max_digits=8, decimal_places=2,
        null=True, blank=True, default=Decimal('0.00'))
    receipt_date = models.DateTimeField(null=True, blank=True)
    units_received = models.DecimalField(max_digits=8, decimal_places=2,
        null=True, blank=True, default=Decimal('0.00'))

    def save(self, *args, **kwargs):

        if self.receipt_date is not None and not self.units_received:
            units_received = (
                self.quantity *
                getattr(self.inventory, 'conversion_factor', Decimal(0.00)))
            self.units_received = units_received

        if self.receipt_date is not None and not self.landed_cost:
            logger.debug('Calculating landed cost...')
            try:
                percentage_cost = self.cost / self.purchase_order.total
                percentage_weight = self.weight / self.purchase_order.weight
            except (ZeroDivisionError, InvalidOperation) as e:
                logger.debug('Cannot calculate landed cost: %s.' % str(e))
            else:
                self.landed_cost = (
                    self.cost +
                    (percentage_cost * self.purchase_order.sales_tax) +
                    (percentage_weight * self.purchase_order.shipping_cost))
                logger.debug('Calculated landed cost as %d.' % self.landed_cost)

        super(Supply, self).save(*args, **kwargs)

    @property
    def weight(self):
        '''
        Return the weight of the Supply.
        '''
        weight = getattr(self.inventory, 'weight', None)
        return (
            self.quantity *
            getattr(self.inventory, 'conversion_factor', Decimal(1.00)) *
            Decimal(getattr(weight, 'g', 0.00)))


    @property
    def unit_cost(self):
        '''
        Return the unit cost of the Supply.
        '''
        logger.debug('Calculating unit cost...')
        cost = Decimal('Infinity')
        try:
            cost = self.landed_cost / self.units_received
            logger.debug('Calculated unit cost as %d.' % cost)
        except (ZeroDivisionError, InvalidOperation) as e:
            logger.debug('Cannot calculate unit cost: %s.' % str(e))

        return cost


    class Meta:
        verbose_name_plural = 'Supplies'
