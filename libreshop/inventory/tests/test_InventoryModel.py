import logging
from datetime import datetime
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from measurement.measures import Weight
from addresses.models import Address
from orders.models import Order, Purchase, Transaction
from products.models import Product, Variant, Component
from ..models import Inventory, PurchaseOrder, Supply, Warehouse

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class InventoryModelTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up Inventory test data.
        self.address = Address.objects.create(
            street_address = '123 Test St',
            locality = 'Test',
            country = 'US')
        self.inventory = Inventory.objects.create(
            name='foo', weight=Weight(g=1.0))
        self.warehouse = Warehouse.objects.create(
            name='foo', address=self.address)

        # Set up Purchase Order test data.
        self.purchase_order = PurchaseOrder.objects.create(
            warehouse=self.warehouse)

        # Set up Product test data.
        product = Product.objects.create(name='foo', sku='123')
        self.variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456')
        component = Component.objects.create(
            variant=self.variant, inventory=self.inventory, quantity=Decimal(1))

        # Set up Purchase test data.
        shipping_address = Address.objects.create(
            street_address = '123 Test St',
            locality = 'Test',
            country = 'US')
        self.order = Order.objects.create(shipping_address=shipping_address)
        transaction = Transaction.objects.create(
            order=self.order, transaction_id='bar')


    def test_model_has_name_field(self):
        '''
        Test that Inventory.name is present.
        '''
        name = getattr(self.inventory, 'name', None)
        self.assertIsNotNone(name)


    def test_model_has_warehouses_field(self):
        '''
        Test that Inventory.warehouses is present.
        '''
        warehouses = getattr(self.inventory, 'warehouses', None)
        self.assertIsNotNone(warehouses)


    def test_model_has_alternatives_field(self):
        '''
        Test that Inventory.alternatives is present.
        '''
        alternatives = getattr(self.inventory, 'alternatives', None)
        self.assertIsNotNone(alternatives)


    def test_saving_to_and_retrieving_inventory_from_the_database(self):
        '''
        Test that an Inventory object can be successfuly saved to the database.
        '''
        inventory = Inventory(name='foo')
        inventory.save()
        num_inventory = Inventory.objects.all().count()
        self.assertEqual(num_inventory, 2)


    def test_components_are_unlinked_when_inventory_is_deleted(self):
        '''
        Test that any linked Components are unlinked when an Inventory object is
        deleted.
        '''
        component = Component.objects.create(variant=self.variant)
        inventory = Inventory.objects.create(name='qux')
        component.inventory = inventory
        component.save()
        inventory.delete()
        num_components = Component.objects.filter(variant=self.variant).count()
        self.assertEqual(num_components, 1)


    def test_model_reports_current_fifo_cost(self):
        '''
        Test that an Inventory object reports its current FIFO cost.
        '''
        # Create common test data.
        tzinfo = timezone.get_current_timezone()

        # Create a Supply from which the cost should be derived.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(12))

        # Create an extra Supply.
        supply2 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(24))

        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        supply.save()

        supply2.receipt_date = datetime(2016, 1, 2, 0, 0, 0, tzinfo=tzinfo)
        supply2.save()

        self.assertEqual(self.inventory.fifo_cost, Decimal(1.00))


    def test_model_reports_fifo_cost_for_partially_depleted_supply(self):
        '''
        Test that an Inventory object reports its current FIFO cost from a
        partially depleted supply.
        '''
        # Create common test data.
        tzinfo = timezone.get_current_timezone()

        # Create a Supply from which the cost should be derived.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(12))

        # Create an extra Supply.
        supply2 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(24))

        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        supply.save()

        supply2.receipt_date=datetime(2016, 1, 2, 0, 0, 0, tzinfo=tzinfo)
        supply2.save()

        # Make a Purchase.
        purchase = Purchase.objects.create(
            order=self.order, variant=self.variant)

        self.assertEqual(self.inventory.fifo_cost, Decimal(1.00))


    def test_model_reports_fifo_cost_for_fully_depleted_supply(self):
        '''
        Test that an Inventory object reports its current FIFO cost from a
        fully depleted supply.
        '''
        # Create common test data.
        tzinfo = timezone.get_current_timezone()

        # Create a Supply that will be depleted.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(12))

        # Create a Supply from which the cost should be derived.
        supply2 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(24))

        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        supply.save()

        supply2.receipt_date=datetime(2016, 1, 2, 0, 0, 0, tzinfo=tzinfo)
        supply2.save()

        # Deplete the first Supply.
        for i in range(12):
            purchase = Purchase.objects.create(
                order=self.order, variant=self.variant)

        self.assertEqual(self.inventory.fifo_cost, Decimal(2.00))


    def test_model_reports_fifo_cost_for_no_supply(self):
        '''
        Test that an Inventory object reports its current FIFO cost when no
        Supply information is available.
        '''
        # Make a Purchase.
        purchase = Purchase.objects.create(
            order=self.order, variant=self.variant)

        self.assertEqual(self.inventory.fifo_cost, Decimal(0.00))


    def test_model_reports_fifo_cost_for_a_given_date(self):
        '''
        Test that an Inventory object reports a FIFO cost for a specific date.
        '''
        # Create common test data.
        tzinfo = timezone.get_current_timezone()

        # Create a Supply for January.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(12))

        # Create a Supply for February.
        supply2 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(24))

        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        supply.save()

        supply2.receipt_date = datetime(2016, 2, 1, 0, 0, 0, tzinfo=tzinfo)
        supply2.save()

        # Deplete the Supply received in January.
        purchase_date = datetime(2016, 1, 31, tzinfo=tzinfo)
        for i in range(12):
            purchase = Purchase.objects.create(
                order=self.order, variant=self.variant, created=purchase_date)

        # Determine the FIFO cost for the end of the month of January.
        fifo_cost = self.inventory.get_fifo_cost(for_date=purchase_date)

        self.assertEqual(fifo_cost, Decimal(1.00))


    def test_model_reports_fifo_cost_when_supplies_are_backordered(self):
        '''
        Test that an Inventory object reports a FIFO cost for a specific date.
        '''
        # Create common test data.
        tzinfo = timezone.get_current_timezone()

        # Create a Supply for January.
        supply = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(12))

        # Create a Supply for February.
        supply2 = Supply.objects.create(purchase_order=self.purchase_order,
            inventory=self.inventory, quantity=Decimal(12), cost=Decimal(24))

        supply.receipt_date = datetime(2016, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        supply.save()

        supply2.receipt_date = datetime(2016, 2, 1, 0, 0, 0, tzinfo=tzinfo)
        supply2.save()

        # Deplete the Supply received in January.
        purchase_date = datetime(2016, 1, 1, tzinfo=tzinfo)
        for i in range(12):
            purchase = Purchase.objects.create(
                order=self.order, variant=self.variant, created=purchase_date)

        # Determine the FIFO cost for the end of the month of January.
        fifo_cost = self.inventory.get_fifo_cost(for_date=purchase_date)

        self.assertEqual(fifo_cost, Decimal(1.00))
