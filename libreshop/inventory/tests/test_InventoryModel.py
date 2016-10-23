import logging
from decimal import Decimal
from django.test import TestCase
from products.models import Product, Variant, Component
from ..models import Inventory

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class InventoryModelTest(TestCase):

    def setUp(self):
        self.inventory = Inventory.objects.create(name='foo')


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


    def test_model_has_cost_field(self):
        '''
        Test that Inventory.alternatives is present.
        '''

        cost = getattr(self.inventory, 'cost', None)
        self.assertIsNotNone(cost)


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
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(product=product, name='bar')
        component = Component.objects.create(variant=variant)
        inventory = Inventory.objects.create(name='qux')
        component.inventory = inventory
        component.save()
        inventory.delete()
        num_components = Component.objects.filter(variant=variant).count()
        self.assertEqual(num_components, 1)
