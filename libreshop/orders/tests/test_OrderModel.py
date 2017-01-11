import logging
from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from addresses.models import Address
from products.models import Product, Variant
from measurement.measures import Weight
from addresses.models import Address
from inventory.models import Inventory, PurchaseOrder, Supply, Warehouse
from products.models import Product, Variant, Component
from ..models import Order, Purchase, Transaction


try:
    # Try to import from the Python 3.3+ standard library.
    from unittest.mock import patch
except ImportError as e:
    # Otherwise, import from the `mock` project dependency.
    from mock import patch

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class OrderModelTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Create common test data.
        self.tzinfo = timezone.get_current_timezone()

        # Set up Inventory test data.
        self.inventory = Inventory.objects.create(
            name='foo', weight=Weight(g=1.0))

        # Set up Purchase Order test data.
        address = Address.objects.create(
            street_address = '123 Test St',
            locality = 'Test',
            country = 'US')
        warehouse = Warehouse.objects.create(name='foo', address=address)
        self.purchase_order = PurchaseOrder.objects.create(warehouse=warehouse)

        # Set up Product test data.
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456')
        component = Component.objects.create(
            variant=variant, inventory=self.inventory, quantity=Decimal(1))

        # Set up test data.
        shipping_address = Address.objects.create(
            street_address = '123 Test St',
            locality = 'Test',
            country = 'US')
        self.order = Order.objects.create(
            token='foo', shipping_address=shipping_address)
        transaction = Transaction.objects.create(
            order=self.order, transaction_id='bar')
        self.purchase = Purchase.objects.create(
            order=self.order, variant=variant)


    @patch('orders.models.order.randrange')
    def test_model_generates_unique_random_order_token(self, randrange_mock):
        '''
        Test that the orders.Order model generates a unique order token.
        '''
        randrange_mock.return_value = 322424845
        order = Order.objects.create()
        self.assertEqual(order.token, '1337d00d')


    def test_model_handles_conflicting_order_tokens(self):
        '''
        Test that the orders.Order model properly handles conflicting token
        requests.
        '''
        order1 = Order.objects.create(token='1337d00d')
        order2 = Order.objects.create(token='1337d00d')
        self.assertNotEqual(order1.token, order2.token)


    def test_fulfilled_property_provides_false_fulfillment_status_when_incomplete(self):
        '''
        Test that the Order.fulfilled property provides a False value when the
        Order fulfillment status is incomplete.
        '''
        fulfilled = getattr(self.order, 'fulfilled', None)
        self.assertFalse(fulfilled)


    def test_fulfilled_property_provides_true_fulfillment_status_when_complete(self):
        '''
        Test that the Order.fulfilled property provides a True value when the
        Order fulfillment status is complete.
        '''
        self.purchase.fulfilled = True
        self.purchase.save()

        fulfilled = getattr(self.order, 'fulfilled', None)
        self.assertTrue(fulfilled)


    def test_cost_of_goods_sold_defaults_to_none(self):
        '''
        Test that Order.cost_of_goods_sold defaults to None.
        '''
        self.assertIsNone(self.order.cost_of_goods_sold)


    def test_cost_property_calculates_cost_of_goods_sold(self):
        '''
        Test that the Order.cost property populates the Order.cost_of_goods_sold
        value when it is called.
        '''
        # Set up a Supply cost.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(1), cost=Decimal(1))
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        # Calcualte Order cost.
        cost = self.order.cost

        self.assertEqual(self.order.cost_of_goods_sold, Decimal(1.00))


    def test_cost_of_goods_sold_is_cached_for_fulfilled_orders(self):
        '''
        Test that the value saved in Order.cost_of_goods_sold is cached for
        fulfilled orders.
        '''
        # Set up a Supply cost.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(1), cost=Decimal(1))
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        # Fulfill Order.
        self.purchase.fulfilled = True
        self.purchase.save()

        # Calcualte Order cost.
        cost = self.order.cost

        # Increase Supply cost.
        supply.receipt_date = None
        supply.units_received = None
        supply.landed_cost = None
        supply.save()
        supply.cost = Decimal(2)
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        # Recalculate Order cost.
        cost2 = self.order.cost

        # Verify that the calculated cost did not change.
        self.assertEqual(cost, cost2)


    def test_cost_of_goods_sold_is_recalculated_for_unfulfilled_orders(self):
        '''
        Test that the value saved in Order.cost_of_goods_sold is recalculated
        for unfulfilled orders.
        '''
        # Set up a Supply cost.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(1), cost=Decimal(1))
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        # Calcualte Order cost.
        cost = self.order.cost

        # Increase Supply cost.
        supply.receipt_date = None
        supply.units_received = None
        supply.landed_cost = None
        supply.save()
        supply.cost = Decimal(2)
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        # Recalculate Order cost.
        cost2 = self.order.cost

        # Verify that the Order cost was recalculated.
        self.assertNotEqual(cost, cost2)


    def test_cost_of_goods_sold_cache_reset(self):
        '''
        Test that the value saved in Order.cost_of_goods_sold is recalculated
        when the cache value is reset.
        '''
        # Set up a Supply cost.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(1), cost=Decimal(1))
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        # Calcualte Order cost.
        cost = self.order.cost

        # Increase Supply cost.
        supply.receipt_date = None
        supply.units_received = None
        supply.landed_cost = None
        supply.save()
        supply.cost = Decimal(2)
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        # Reset cached value.
        self.order.cost_of_goods_sold = None
        self.order.save()

        # Recalculate Order cost.
        cost2 = self.order.cost

        # Verify that the calculated cost did not change.
        self.assertEqual(self.order.cost_of_goods_sold, Decimal(2))
