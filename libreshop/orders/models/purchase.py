import logging
from collections import OrderedDict
from decimal import Decimal
from itertools import groupby
from django.db import models
from django.db.models import BooleanField, Case, Count, Sum, When
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

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
        if self.variant.fulfillment_settings:
            try:
                # Try to get the total cost of a backend drop-shipment Purchase.
                cost = self.fulfillment_purchase.total
                logger.debug('Purchase has been submitted for fulfillment.')
            except FulfillmentPurchase.DoesNotExist as e:
                logger.debug('Purchase has been not submitted for fulfillment.')

        else:
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
            'Cost of the "%s" Purchase under Order "%s" is %s.' %
            (self.variant.name, self.order.token, cost))

        return cost
