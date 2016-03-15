from datetime import datetime
from decimal import Decimal
from random import randrange
from django.core.validators import MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel


def get_token(token=None):
    generate = lambda: '{:08x}'.format(randrange(2**32))
    if not token:
        token = generate()
    while Order.objects.filter(token=token):
        token = generate()
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

    objects = OrderManager()


class Transaction(TimeStampedModel):
    order = models.ForeignKey('Order', null=True, blank=True)
    transaction_id = models.CharField(
        max_length=8, null=False, blank=False, unique=True, verbose_name='ID'
    )
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, blank=False,
        default=Decimal('0.00')
    )
    cardholder_name = models.CharField(max_length=64, null=True, blank=True)
    payment_card_type = models.CharField(max_length=8, null=True, blank=True)
    payment_card_last_4 = models.CharField(
        max_length=8, null=True, blank=True, verbose_name='Last 4'
    )
    created_at = models.DateTimeField(default=datetime.now)
    origin_ip_address = models.GenericIPAddressField(null=False, blank=False)
    authorized = models.BooleanField(default=False)


class Purchase(TimeStampedModel):
    order = models.ForeignKey('orders.Order', null=False)
    variant = models.ForeignKey('products.Variant', null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False,
            blank=False, default=Decimal('0.00'))
    fulfilled = models.BooleanField(default=False)


class TaxRate(TimeStampedModel):

    state = models.CharField(max_length=4, null=True, blank=True)
    district = models.CharField(max_length=4, null=True, blank=True)
    county = models.CharField(max_length=4, null=True, blank=True)
    city = models.CharField(max_length=4, null=True, blank=True)
    postal_code = models.CharField(max_length=16, null=True, blank=True)


    state_tax_rate = models.DecimalField(max_digits=5, decimal_places=4,
        null=False, blank=False, default=Decimal('0.00'))
    district_tax_rate = models.DecimalField(max_digits=5, decimal_places=4,
        null=False, blank=False, default=Decimal('0.00'))
    county_tax_rate = models.DecimalField(max_digits=5, decimal_places=4,
        null=False, blank=False, default=Decimal('0.00'))
    local_tax_rate = models.DecimalField(max_digits=5, decimal_places=4,
        null=False, blank=False, default=Decimal('0.00'))

    @property
    def tax_rate(self):
        return (
            self.local_tax_rate + self.county_tax_rate +
            self.district_tax_rate + self.state_tax_rate
        )
