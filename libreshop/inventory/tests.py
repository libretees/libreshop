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
from .models import Inventory, Location, Warehouse

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class WarehouseModelTest(TestCase):

    def test_model_has_name_field(self):
        '''
        Test that Warehouse.name is present.
        '''
        warehouse = Warehouse.objects.create(name='foo',
            address=Address.objects.create())
        name = getattr(warehouse, 'name', None)
        self.assertIsNotNone(name)


    def test_model_has_address_field(self):
        '''
        Test that Warehouse.address is present.
        '''
        warehouse = Warehouse.objects.create(name='foo',
            address=Address.objects.create())
        address = getattr(warehouse, 'address', None)
        self.assertIsNotNone(address)


    def test_saving_to_and_retrieving_warehouses_from_the_database(self):
        '''
        Test that a Warehouse can be successfuly saved to the database.
        '''
        warehouse = Warehouse(name='foo', address=Address.objects.create())
        warehouse.save()
        num_warehouses = Warehouse.objects.all().count()
        self.assertEqual(num_warehouses, 1)


    def test_name_field_is_required(self):
        '''
        Test that Warehouse.name is required.
        '''
        func = Warehouse.objects.create
        self.assertRaises(IntegrityError, func, name=None,
            address=Address.objects.create())


    def test_address_field_is_required(self):
        '''
        Test that Warehouse.address is required.
        '''
        func = Warehouse.objects.create
        self.assertRaises(ValueError, func, name='foo', address=None)


    def test_name_field_must_be_unique(self):
        '''
        Test that Warehouse.name must be unique.
        '''
        warehouse = Warehouse.objects.create(name='foo',
            address=Address.objects.create())
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='foo',
            address=Address.objects.create())


    def test_name_field_must_be_unique_regardless_of_character_case(self):
        '''
        Test that Warehouse.name must be unique regardless of character case.
        '''
        warehouse = Warehouse.objects.create(name='foo',
            address=Address.objects.create())
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='Foo',
            address=Address.objects.create())


    def test_name_and_address_field_must_be_unique_together(self):
        '''
        Test that Warehouse.name and Warehouse.address must be unique together.
        '''
        address = Address.objects.create()
        warehouse = Warehouse.objects.create(name='foo', address=address)
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='foo', address=address)


    def test_address_field_must_be_unique(self):
        '''
        Test that Warehouse.address must be unique.
        '''
        address = Address.objects.create()
        warehouse = Warehouse.objects.create(name='foo', address=address)
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='bar', address=address)


    def test_name_field_is_correct_length(self):
        '''
        Test that Warehouse.name must be less than or equal to 64 characters in
        length.

        Note that sqlite does not enforce VARCHAR field length constraints.
        '''
        max_length = 64
        database_engine = settings.DATABASES['default']['ENGINE']
        random_string = (''.join(random.choice(string.ascii_letters +
            string.digits) for _ in range(max_length+1)))
        if database_engine != 'django.db.backends.sqlite3':
            func = Warehouse.objects.create
            self.assertRaises(IntegrityError, func, name=random_string,
                address=Address.objects.create())


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


class InventoryModelTest(TestCase):

    def test_model_has_name_field(self):
        '''
        Test that Inventory.name is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        name = getattr(inventory, 'name', None)
        self.assertIsNotNone(name)


    def test_model_has_warehouses_field(self):
        '''
        Test that Inventory.warehouses is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        warehouses = getattr(inventory, 'warehouses', None)
        self.assertIsNotNone(warehouses)


    def test_model_has_alternatives_field(self):
        '''
        Test that Inventory.alternatives is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        alternatives = getattr(inventory, 'alternatives', None)
        self.assertIsNotNone(alternatives)


    def test_model_has_cost_field(self):
        '''
        Test that Inventory.alternatives is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        cost = getattr(inventory, 'cost', None)
        self.assertIsNotNone(cost)


    def test_saving_to_and_retrieving_inventory_from_the_database(self):
        '''
        Test that an Inventory object can be successfuly saved to the database.
        '''
        inventory = Inventory(name='foo')
        inventory.save()
        num_inventory = Inventory.objects.all().count()
        self.assertEqual(num_inventory, 1)


    def test_components_are_unlinked_when_inventory_is_deleted(self):
        '''
        Test that any linked Components are unlinked when an Inventory object is
        deleted.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(product=product, name='bar')
        component = Component.objects.create(variant=variant)
        inventory = Inventory.objects.create(name='qux')
        component.inventory = inventory
        component.save()
        inventory.delete()
        num_components = Component.objects.filter(variant=variant).count()
        self.assertEqual(num_components, 1)
