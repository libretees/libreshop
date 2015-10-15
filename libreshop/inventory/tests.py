import string
import random
import logging
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from shop.models import Address
from inventory.models import (Warehouse, Attribute, Inventory, Attribute_Value,
    Location)

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


class AttributeModelTest(TestCase):

    def test_model_has_name_field(self):
        '''
        Test that Attribute.name is present.
        '''
        attribute = Attribute.objects.create(name='foo')
        name = getattr(attribute, 'name', None)
        self.assertIsNotNone(name)


    def test_saving_to_and_retrieving_attributes_from_the_database(self):
        '''
        Test that an Attribute can be successfuly saved to the database.
        '''
        attribute = Attribute(name='foo')
        attribute.save()
        num_attributes = Attribute.objects.all().count()
        self.assertEqual(num_attributes, 1)


    def test_name_field_is_required(self):
        '''
        Test that Attribute.name is required.
        '''
        func = Attribute.objects.create
        self.assertRaises(IntegrityError, func, name=None)


    def test_name_field_must_be_unique(self):
        '''
        Test that Attribute.name must be unique.
        '''
        attribute = Attribute.objects.create(name='foo')
        func = Attribute.objects.create
        self.assertRaises(ValidationError, func, name='foo')


    def test_name_field_must_be_unique_regardless_of_character_case(self):
        '''
        Test that Attribute.name must be unique regardless of character case.
        '''
        attribute = Attribute.objects.create(name='foo')
        func = Attribute.objects.create
        self.assertRaises(ValidationError, func, name='Foo')


    def test_name_field_is_correct_length(self):
        '''
        Test that Attribute.name must be less than or equal to 64 characters in
        length.

        Note that sqlite does not enforce VARCHAR field length constraints.
        '''
        max_length = 64
        database_engine = settings.DATABASES['default']['ENGINE']
        random_string = (''.join(random.choice(string.ascii_letters +
            string.digits) for _ in range(max_length+1)))
        func = Attribute.objects.create
        if database_engine != 'django.db.backends.sqlite3':
            self.assertRaises(IntegrityError, func, name=random_string)


class AttributeValueModelTest(TestCase):

    def test_model_has_inventory_field(self):
        '''
        Test that Attribute_Value.inventory is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        attribute = Attribute.objects.create(name='bar')
        attribute_value = Attribute_Value.objects.create(attribute=attribute,
            inventory=inventory, value='baz')
        inventory = getattr(attribute_value, 'inventory', None)
        self.assertIsNotNone(inventory)


    def test_model_has_attribute_field(self):
        '''
        Test that Attribute_Value.attribute is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        attribute = Attribute.objects.create(name='bar')
        attribute_value = Attribute_Value.objects.create(attribute=attribute,
            inventory=inventory, value='baz')
        attribute = getattr(attribute_value, 'attribute', None)
        self.assertIsNotNone(attribute)


    def test_model_has_value_field(self):
        '''
        Test that Attribute_Value.value is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        attribute = Attribute.objects.create(name='bar')
        attribute_value = Attribute_Value.objects.create(attribute=attribute,
            inventory=inventory, value='baz')
        value = getattr(attribute_value, 'value', None)
        self.assertIsNotNone(value)


    def test_saving_to_and_retrieving_attribute_values_from_the_database(self):
        '''
        Test that an Attribute Value can be successfuly saved to the database.
        '''
        inventory = Inventory.objects.create(name='foo')
        attribute = Attribute.objects.create(name='bar')
        attribute_value = Attribute_Value(attribute=attribute,
            inventory=inventory, value='baz')
        attribute_value.save()
        num_attribute_values = Attribute_Value.objects.all().count()
        self.assertEqual(num_attribute_values, 1)


    def test_inventory_can_have_multiple_unique_attributes(self):
        '''
        Test that multiple distinct Attributes can be associated to an Inventory
        object.
        '''
        inventory = Inventory.objects.create(name='foo')
        attribute1 = Attribute.objects.create(name='bar')
        attribute2 = Attribute.objects.create(name='baz')
        attribute_value1 = Attribute_Value.objects.create(attribute=attribute1,
            inventory=inventory, value='qux')
        attribute_value2 = Attribute_Value.objects.create(attribute=attribute2,
            inventory=inventory, value='quux')
        num_associated_attributes = (Attribute_Value.objects.
            filter(inventory=inventory).count())
        self.assertEqual(num_associated_attributes, 2)


    def test_inventory_cannot_have_multiple_similar_attributes(self):
        '''
        Test that multiple similar Attributes cannot be associated to an
        Inventory object.
        '''
        inventory = Inventory.objects.create(name='foo')
        attribute = Attribute.objects.create(name='bar')
        attribute_value = Attribute_Value.objects.create(attribute=attribute,
            inventory=inventory, value='baz')
        func = Attribute_Value.objects.create
        self.assertRaises(IntegrityError, func, attribute=attribute,
            inventory=inventory, value='qux')


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


    def test_model_has_attributes_field(self):
        '''
        Test that Inventory.attributes is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        attributes = getattr(inventory, 'attributes', None)
        self.assertIsNotNone(attributes)


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
