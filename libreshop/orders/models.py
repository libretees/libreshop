import logging
from collections import Counter, OrderedDict
from decimal import Decimal
from random import randrange
from itertools import groupby
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import BooleanField, Case, Count, Sum, When
from django.utils import timezone
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

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

    @property
    def cost(self):
        return self.cost_of_goods_sold

    @property
    def cost_of_goods_sold(self):
        return sum(purchase.cost for purchase in self.purchases.all())

    def __str__(self):
        return self.token


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
        max_length=16, null=True, blank=True, verbose_name='Card Type'
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


class PurchaseManager(models.Manager):
    def get_queryset(self):
        queryset = super(PurchaseManager, self).get_queryset()
        queryset = queryset.annotate(
            variant_settings=Count('variant__fulfillmentsettingvalue'),
            product_settings=Count('variant__product__fulfillmentsettingvalue'))
        queryset = queryset.annotate(
            drop_shipped=Case(
                When(variant_settings__gt=0, then=True),
                When(product_settings__gt=0, then=True),
                default=False,
                output_field=BooleanField()))
        return queryset


class Purchase(TimeStampedModel):
    order = models.ForeignKey(
        'orders.Order', null=False, related_name='purchases')
    variant = models.ForeignKey('products.Variant', null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False,
            blank=False, default=Decimal('0.00'))
    fulfilled = models.BooleanField(default=False)

    objects = PurchaseManager()

    @property
    def cost(self):
        '''
        Shortcut for `cost_of_goods_sold` property.
        '''
        return self.cost_of_goods_sold

    @property
    def cost_of_goods_sold(self):
        '''
        The Cost of Goods Sold (COGS) of the Purchase.
        '''
        from fulfillment.models import FulfillmentPurchase
        from inventory.models import Supply

        cost = Decimal(0.00)

        # Determine whether or not this is a drop-shipped Purchase.
        try:
            # Try to get the total cost of a backend drop-shipment Purchase.
            cost = self.fulfillment_purchase.total
            logger.debug('Purchase is drop-shipped to customer.')
        except FulfillmentPurchase.DoesNotExist as e:
            logger.debug('Purchase is manufactured in-house.')

            # Determine the amount of each respective raw material in Inventory
            # that is consumed to produce this Purchase.

            inventory_consumed = {
                component.inventory:component.quantity
                for component in self.variant.components.all()}
            logger.debug(
                'Inventory consumed by this Purchase: %s' % inventory_consumed)

            # Determine the amount of all raw materials taken from Inventory
            # prior to this Purchase.

            prior_inventory_consumed = [
                (component.inventory, component.quantity)
                for purchases
                    in Purchase.objects.filter(created__lt=self.created)
                for component in purchases.variant.components.filter(
                    inventory__in=inventory_consumed)]
            prior_inventory_aggregate = {
                inventory:sum(quantity[1] for quantity in quantities)
                for (inventory, quantities)
                in groupby(sorted(prior_inventory_consumed), lambda x: x[0])}
            logger.debug(
                'Inventory consumed before this Purchase: %s' %
                prior_inventory_aggregate)

            # Determine the range of Inventory consumed by this Purchase
            # with respect to incoming Supply.

            inventory_consumed_ranges = {
                inventory:(
                    prior_inventory_aggregate.get(inventory, Decimal(0.00)),
                    prior_inventory_aggregate.get(inventory, Decimal(0.00)) +
                    value)
                for (inventory, value) in inventory_consumed.items()}

            logger.debug(
                'Inventory ranges consumed by this Purchase: %s' %
                inventory_consumed_ranges)

            # Calculate the cost of goods sold for this Purchase.
            for inventory, range_ in inventory_consumed_ranges.items():

                # Create a number line of all Supply received for this
                # particular raw material, along with its associated unit cost.

                supplies = Supply.objects.filter(
                    inventory=inventory, receipt_date__isnull=False)
                price_history = {(
                    sum(supply.units_received for supply in supplies[:i]),
                    sum(supply.units_received for supply in supplies[:i]) +
                    supply.units_received): supply.unit_cost
                    for (i, supply) in enumerate(supplies)}
                price_history = OrderedDict(
                    sorted(price_history.items(), key=lambda x: x[0]))

                logger.debug(
                    'Price history for %s is: %s' % (inventory, price_history))

                # Associate the number line with the range of Supply consumed
                # by this Purchase.

                purchase_start, purchase_end = range_
                for range_, unit_cost in price_history.items():
                    units_from_supply = 0
                    supply_start, supply_end = range_

                    # If the Supply was consumed already, continue searching.
                    if supply_end < purchase_start:
                        continue

                    # The Purchase is manufactured from a single Supply.
                    elif supply_start <= purchase_start < purchase_end <= supply_end:
                        units_from_supply = inventory_consumed[inventory]

                    # The entire Supply is used to manufacture the Purchase.
                    elif purchase_start <= supply_start < supply_end <= purchase_end:
                        units_from_supply = supply_end - supply_start

                    # The Purchase consumes the remainder of a Supply.
                    elif supply_start <= purchase_start <= supply_end:
                        units_from_supply = supply_end - purchase_start

                    # The Purchase consumes part of a Supply
                    elif supply_start <= purchase_end <= supply_end:
                        units_from_supply = purchase_end - supply_start

                    # Undefined behavior.
                    else:
                        logger.debug((
                            'Undefined scenario occured for Supply(%s,%s] '
                            'Purchase(%s,%s]') % (
                                supply_start, supply_end,
                                purchase_start, purchase_end))

                    # Add the Supply unit cost to the cost of the Purchase.
                    cost += units_from_supply * unit_cost

                    # Stop calculation if all Inventory is accounted for.
                    inventory_consumed[inventory] -= units_from_supply
                    if inventory_consumed[inventory] <= 0:
                        break

                logger.info(
                    'Cost of the "%s" Purchase is: %s' %
                    (self.variant.name, cost))

        return cost


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

    def __str__(self):
        return '%s, %s %s' % (self.city, self.state, self.postal_code)

    class Meta:
        verbose_name = 'Tax Rate'
        unique_together = ('state', 'district', 'county', 'city', 'postal_code')



class Communication(TimeStampedModel):
    order = models.ForeignKey('Order', null=True, blank=True)
    from_email = models.EmailField(null=False, blank=False)
    to_email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=998, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
