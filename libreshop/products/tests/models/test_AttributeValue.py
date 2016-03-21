import logging
from django.db.utils import IntegrityError
from django.test import TestCase
from ...models import Attribute, AttributeValue, Product, Variant

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class AttributeValueModelTest(TestCase):

    def test_model_has_inventory_field(self):
        '''
        Test that AttributeValue.variant is present.
        '''
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(product=product, name='bar')
        attribute = Attribute.objects.create(name='foo')
        attribute_value = AttributeValue.objects.create(
            variant=variant, attribute=attribute, value='bar'
        )

        inventory = getattr(attribute_value, 'variant', None)
        self.assertIsNotNone(inventory)


    def test_model_has_attribute_field(self):
        '''
        Test that AttributeValue.attribute is present.
        '''
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(product=product, name='bar')
        attribute = Attribute.objects.create(name='foo')
        attribute_value = AttributeValue.objects.create(
            variant=variant, attribute=attribute, value='bar'
        )

        attribute = getattr(attribute_value, 'attribute', None)
        self.assertIsNotNone(attribute)


    def test_model_has_value_field(self):
        '''
        Test that AttributeValue.value is present.
        '''
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(product=product, name='bar')
        attribute = Attribute.objects.create(name='foo')
        attribute_value = AttributeValue.objects.create(
            variant=variant, attribute=attribute, value='bar'
        )

        value = getattr(attribute_value, 'value', None)
        self.assertIsNotNone(value)


    def test_model_has_name_property(self):
        '''
        Test that AttributeValue.name is present.
        '''
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(product=product, name='bar')
        attribute = Attribute.objects.create(name='foo')
        attribute_value = AttributeValue.objects.create(
            variant=variant, attribute=attribute, value='bar'
        )

        name = getattr(attribute_value, 'name', None)
        self.assertIsNotNone(name)


    def test_saving_to_and_retrieving_attribute_values_from_the_database(self):
        '''
        Test that an Attribute Value can be successfuly saved to the database.
        '''
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(product=product, name='bar')
        attribute = Attribute.objects.create(name='foo')

        attribute_value = AttributeValue(
            variant=variant, attribute=attribute, value='bar'
        )
        attribute_value.save()

        num_attribute_values = AttributeValue.objects.all().count()
        self.assertEqual(num_attribute_values, 1)


    def test_variant_can_have_multiple_unique_attributes(self):
        '''
        Test that multiple distinct Attributes can be associated to a Variant
        object.
        '''
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(product=product, name='bar')
        attribute1 = Attribute.objects.create(name='bar')
        attribute2 = Attribute.objects.create(name='baz')
        attribute_value1 = AttributeValue.objects.create(
            variant=variant, attribute=attribute1, value='qux'
        )
        attribute_value2 = AttributeValue.objects.create(
            variant=variant, attribute=attribute2, value='quux'
        )
        num_associated_attributes = (
            AttributeValue.objects.filter(variant=variant).count()
        )
        self.assertEqual(num_associated_attributes, 2)


    def test_variant_cannot_have_multiple_similar_attributes(self):
        '''
        Test that multiple similar Attributes cannot be associated to an Variant
        object.
        '''
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(product=product, name='bar')
        attribute = Attribute.objects.create(name='foo')
        attribute_value = AttributeValue.objects.create(
            variant=variant, attribute=attribute, value='bar'
        )

        func = AttributeValue.objects.create
        self.assertRaises(
            IntegrityError, func, variant=variant, attribute=attribute,
            value='qux'
        )
