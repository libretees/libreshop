import logging
from django.test import TestCase
from inventory.models import Inventory
from ...models import Attribute, Attribute_Value

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
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


    def test_model_has_name_property(self):
        '''
        Test that Attribute_Value.name is present.
        '''
        inventory = Inventory.objects.create(name='foo')
        attribute = Attribute.objects.create(name='bar')
        attribute_value = Attribute_Value.objects.create(attribute=attribute,
            inventory=inventory, value='baz')
        name = getattr(attribute_value, 'name', None)
        self.assertIsNotNone(name)


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
