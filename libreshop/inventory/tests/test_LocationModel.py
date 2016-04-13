import string
import random
import logging
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from products.models import Product, Variant, Component
from addresses.models import Address
from ..models import Inventory, Location, Warehouse

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class LocationModelTest(TestCase):

    def test_model_has_inventory_field(self):
        '''
        Test that Location.inventory is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        warehouse = Warehouse.objects.create(name='bar',
            address=Address.objects.create())
        location = Location.objects.create(warehouse=warehouse,
            inventory=inventory, quantity=Decimal(0.00))
        inventory = getattr(location, 'inventory', None)
        self.assertIsNotNone(inventory)


    def test_model_has_warehouse_field(self):
        '''
        Test that Location.warehouse is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        warehouse = Warehouse.objects.create(name='bar',
            address=Address.objects.create())
        location = Location.objects.create(warehouse=warehouse,
            inventory=inventory, quantity=Decimal(0.00))
        warehouse = getattr(location, 'warehouse', None)
        self.assertIsNotNone(warehouse)


    def test_model_has_quantity_field(self):
        '''
        Test that Location.quantity is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        warehouse = Warehouse.objects.create(name='bar',
            address=Address.objects.create())
        location = Location.objects.create(warehouse=warehouse,
            inventory=inventory, quantity=Decimal(0.00))
        quantity = getattr(location, 'quantity', None)
        self.assertIsNotNone(quantity)


    def test_saving_to_and_retrieving_locations_from_the_database(self):
        '''
        Test that a Location can be successfuly saved to the database.
        '''
        inventory = Inventory.objects.create(name='foo')
        warehouse = Warehouse.objects.create(name='bar',
            address=Address.objects.create())
        location = Location(warehouse=warehouse, inventory=inventory,
            quantity=Decimal(0.00))
        location.save()
        num_locations = Location.objects.all().count()
        self.assertEqual(num_locations, 1)


    def test_inventory_can_have_multiple_unique_warehouses(self):
        '''
        Test that multiple distinct Warehouses can be associated to an Inventory
        object.
        '''
        inventory = Inventory.objects.create(name='foo')
        warehouse1 = Warehouse.objects.create(name='bar',
            address=Address.objects.create())
        warehouse2 = Warehouse.objects.create(name='baz',
            address=Address.objects.create())
        location1 = Location.objects.create(inventory=inventory,
            warehouse=warehouse1, quantity=Decimal(0.00))
        location2 = Location.objects.create(inventory=inventory,
            warehouse=warehouse2, quantity=Decimal(0.00))
        num_associated_locations = (Location.objects.
            filter(inventory=inventory).count())
        self.assertEqual(num_associated_locations, 2)


    def test_inventory_cannot_have_multiple_similar_warehouses(self):
        '''
        Test that multiple similar Warehouses cannot be associated to an
        Inventory object.
        '''
        inventory = Inventory.objects.create(name='foo')
        warehouse = Warehouse.objects.create(name='bar',
            address=Address.objects.create())
        location = Location.objects.create(inventory=inventory,
            warehouse=warehouse, quantity=Decimal(0.00))
        func = Location.objects.create
        self.assertRaises(IntegrityError, func, inventory=inventory,
            warehouse=warehouse, quantity=Decimal(0.00))
