import logging
from django.test import TestCase
from inventory.models import Inventory, Attribute, Attribute_Value
from ..forms import ProductOrderForm
from ..models import Product, Variant, Component

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class ProductOrderFormTest(TestCase):
    def test_form_does_not_create_markup_for_non_salable_product(self):
        '''
        Test that no markup is created for a Product that is not salable.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        form = ProductOrderForm(product)
        self.assertEqual(str(form), '')

    def test_form_does_not_create_markup_for_salable_with_no_attributes(self):
        '''
        Test that no markup is created for a salable Product with no
        attributes.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        inventory = Inventory.objects.create(name='bar')
        variant = Variant.objects.get(product=product)
        component = Component.objects.get(variant=variant)
        component.inventory = inventory
        component.save()
        form = ProductOrderForm(product)
        self.assertEqual(str(form), '')

    def test_form_does_creates_markup_for_salable_product_with_attributes(self):
        '''
        Test that markup is created for a salable Product with linked
        attributes.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        inventory = Inventory.objects.create(name='bar')
        attribute = Attribute.objects.create(name='foo')
        attribute_value = Attribute_Value.objects.create(attribute=attribute,
            inventory=inventory, value='bar')
        variant = Variant.objects.get(product=product)
        component = Component.objects.get(variant=variant)
        component.inventory = inventory
        component.save()
        form = ProductOrderForm(product)
        markup = ('<tr><th><label for="id_foo">Foo:</label></th><td>' +
            '<select id="id_foo" name="foo">\n' +
            '<option value="bar">bar</option>\n</select></td></tr>')
        self.assertEqual(str(form), markup)
