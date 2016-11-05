import logging
from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from measurement.measures import Weight
from addresses.models import Address
from inventory.models import Inventory, PurchaseOrder, Supply, Warehouse
from products.models import Product, Variant, Component
from ..models import Order, Purchase, Transaction

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class PurchaseModelTest(TestCase):

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
        self.variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456')
        component = Component.objects.create(
            variant=self.variant, inventory=self.inventory, quantity=Decimal(1))

        # Set up test data.
        shipping_address = Address.objects.create(
            street_address = '123 Test St',
            locality = 'Test',
            country = 'US')
        self.order = Order.objects.create(shipping_address=shipping_address)
        transaction = Transaction.objects.create(
            order=self.order, transaction_id='bar')


    def test_model_calculates_cost_for_raw_materials_sourced_from_initial_supply(self):
        '''
        Test that a Purchase.cost can be calculated from an initial Supply
        received.
        '''
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(1), cost=Decimal(1))
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        purchase = Purchase.objects.create(
            order=self.order, variant=self.variant)

        self.assertEqual(purchase.cost, Decimal(1.00))


    def test_model_calculates_cost_for_raw_materials_sourced_from_secondary_supply(self):
        '''
        Test that a Purchase.cost can be calculated from secondary Supplies
        received.
        '''
        # Create a Supply for January.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(1), cost=Decimal(1))

        # Create a Supply for February.
        supply2 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(1), cost=Decimal(2))

        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        supply2.receipt_date = datetime(2016, 2, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply2.save()

        # Deplete the Supply received in January.
        purchase_date = datetime(2016, 1, 2, tzinfo=self.tzinfo)
        purchase = Purchase.objects.create(
            order=self.order, variant=self.variant, created=purchase_date)

        purchase2 = Purchase.objects.create(
            order=self.order, variant=self.variant)

        self.assertEqual(purchase2.cost, Decimal(2.00))


    def test_model_calculates_cost_for_raw_materials_sourced_from_partially_depleted_supply(self):
        '''
        Test that a Purchase.cost can be calculated from a partially depleted
        Supply.
        '''
        # Create a Supply.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(2), cost=Decimal(2))
        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()

        # Partially deplete the Supply.
        purchase_date = datetime(2016, 1, 2, tzinfo=self.tzinfo)
        purchase = Purchase.objects.create(
            order=self.order, variant=self.variant, created=purchase_date)

        purchase2 = Purchase.objects.create(
            order=self.order, variant=self.variant)

        self.assertEqual(purchase2.cost, Decimal(1.00))


    def test_model_calculates_cost_for_raw_materials_sourced_from_fractional_supplies(self):
        '''
        Test that a Purchase.cost can be calculated from a multiple fractional
        Supplies.
        '''
        # Create a half-unit Supply.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(0.5), cost=Decimal(1))

        # Create a half-unit Supply.
        supply2 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(0.5), cost=Decimal(1))

        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.save()
        supply2.receipt_date = datetime(2016, 2, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply2.save()

        purchase = Purchase.objects.create(
            order=self.order, variant=self.variant)
        self.assertEqual(purchase.cost, Decimal(2.00))


    def test_model_calculates_cost_for_raw_materials_sourced_from_combination_of_supplies(self):
        '''
        Test that a Purchase.cost can be calculated from a partially depleted
        Supply and from a fraction of a later Supply.
        '''
        # Create a quarter-unit Supply.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(0.25), cost=Decimal(1))

        # Create a half-unit Supply.
        supply2 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(0.5), cost=Decimal(1))

        # Create a single-unit Supply.
        supply3 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(1), cost=Decimal(1))

        # Create a half-unit Supply.
        supply4 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(0.5), cost=Decimal(1))

        # Create a quarter-unit Supply.
        supply5 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(0.25), cost=Decimal(1))

        receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=self.tzinfo)
        supply.receipt_date = receipt_date
        supply.save()
        supply2.receipt_date = receipt_date
        supply2.save()
        supply3.receipt_date = receipt_date
        supply3.save()
        supply4.receipt_date = receipt_date
        supply4.save()
        supply5.receipt_date = receipt_date
        supply5.save()

        # Deplete Supply 1 & 2 and partially Deplete Supply 3.
        purchase_date = datetime(2016, 1, 2, tzinfo=self.tzinfo)
        purchase = Purchase.objects.create(
            order=self.order, variant=self.variant, created=purchase_date)

        purchase2 = Purchase.objects.create(
            order=self.order, variant=self.variant)

        self.assertEqual(purchase2.cost, Decimal(1.25))
