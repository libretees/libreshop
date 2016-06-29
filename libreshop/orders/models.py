from decimal import Decimal
from random import randrange
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
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


    @property
    def fulfilled(self):
        purchases = Purchase.objects.filter(order=self)
        return all(purchase.fulfilled for purchase in purchases)


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
    country = models.CharField(max_length=2, null=True, blank=True)
    payment_card_type = models.CharField(
        max_length=8, null=True, blank=True, verbose_name='Card Type'
    )
    payment_card_last_4 = models.CharField(
        max_length=8, null=True, blank=True, verbose_name='Last 4'
    )
    payment_card_expiration_date = models.CharField(
        max_length=8, null=True, blank=True, verbose_name='Expiration Date',
        validators=[RegexValidator(
            r'^(0[1-9]|1[0-2])[/-]\d{2}$',
            message='Expiration date must be in MM/YY or MM-YY format',
            code='Invalid expiration date'
        )]
    )
    created_at = models.DateTimeField(default=timezone.now)
    origin_ip_address = models.GenericIPAddressField(null=True, blank=True)
    authorized = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'created_at'


class Purchase(TimeStampedModel):
    order = models.ForeignKey(
        'orders.Order', null=False, related_name='purchases')
    variant = models.ForeignKey('products.Variant', null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False,
            blank=False, default=Decimal('0.00'))
    fulfilled = models.BooleanField(default=False)

    @property
    def name(self):
        return self.variant.name

    @property
    def sku(self):
        return self.variant.sku


class TaxRate(TimeStampedModel):

    state = models.CharField(max_length=64, null=True, blank=True)
    district = models.CharField(max_length=64, null=True, blank=True)
    county = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
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


class Communication(TimeStampedModel):
    order = models.ForeignKey('Order', null=True, blank=True)
    from_email = models.EmailField(null=False, blank=False)
    to_email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=998, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
