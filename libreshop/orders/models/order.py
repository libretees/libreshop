import logging
from decimal import Decimal
from random import randrange
from django.db import models
from model_utils.models import TimeStampedModel
from .purchase import Purchase

# Initialize logger.
logger = logging.getLogger(__name__)

def get_token(token=None):
    generate = lambda: '{:08x}'.format(randrange(2**32))
    if not token:
        logger.debug('Generating token...')
        token = generate()
    while Order.objects.filter(token=token):
        token = generate()

    logger.debug('Generated token (%s).' % token)

    return token

# Create your models here.
class OrderManager(models.Manager):

    def create(self, *args, **kwargs):

        token = kwargs.pop('token', None)
        kwargs.update({
            'token': get_token(token=token)
        })
        return super(OrderManager, self).create(*args, **kwargs)


class Order(TimeStampedModel):

    customer = models.ForeignKey('customers.Customer', null=True, blank=True)
    shipping_address = models.ForeignKey('addresses.Address', null=True,
        blank=True)
    token = models.CharField(max_length=8, null=False, blank=False, unique=True,
        default=get_token)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, null=False,
        blank=False, default=Decimal('0.00'))
    sales_tax = models.DecimalField(max_digits=8, decimal_places=2, null=False,
        blank=False, default=Decimal('0.00'))
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2,
        null=False, blank=False, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=8, decimal_places=2, null=False,
        blank=False, default=Decimal('0.00'))
    cost_of_goods_sold = models.DecimalField(max_digits=8, decimal_places=2,
        null=True, blank=True)

    objects = OrderManager()

    @property
    def fulfilled(self):
        purchases = Purchase.objects.filter(order=self)
        return all(purchase.fulfilled for purchase in purchases)

    @property
    def cost(self):
        if (self.cost_of_goods_sold is None) or not self.fulfilled:
            self.cost_of_goods_sold = sum(
                purchase.cost for purchase in self.purchases.all())

            if self.fulfilled:
                self.save()

        return self.cost_of_goods_sold

    def __str__(self):
        return self.token
