import logging
from django.http import HttpRequest
from django.test import TestCase
from inventory.models import Inventory
from ...forms import ProductOrderForm
from ...models import Attribute, Attribute_Value, Product, Variant, Component

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
        form = ProductOrderForm(product)
        self.assertEqual(str(form), '')


    def test_form_does_not_create_markup_for_salable_product_with_attributes_and_no_options(self):
        '''
        Test that no markup is created for a salable Product with linked
        attributes that do not have multiple values.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        form = ProductOrderForm(product)
        self.assertEqual(str(form), '')


    def test_form_creates_select_markup_for_salable_product_with_multivariate_attribute(self):
        '''
        Test that <select> tag markup is created for a salable Product with
        linked multivariate attributes.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        form = ProductOrderForm(product)

        markup = '<select id="id_foo" name="foo">'

        self.assertIn(markup, str(form))


    def test_form_creates_options_markup_for_salable_product_with_multivariate_attribute(self):
        '''
        Test that <option> tag markup is created for a salable Product with
        linked multivariate attributes.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        form = ProductOrderForm(product)

        markup = (
            '<option value="bar">bar</option>\n' +
            '<option value="baz">baz</option>\n'
        )

        self.assertIn(markup, str(form))


    def test_form_creates_options_markup_maintains_same_character_case_as_attribute_value(self):
        '''
        Test that <option> tag value and inner HTML maintain the same character
        case throughout.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        form = ProductOrderForm(product)

        markup = (
            '<option value="BaR">BaR</option>\n' +
            '<option value="BaZ">BaZ</option>\n'
        )

        self.assertIn(markup, str(form))


    def test_form_markup_creates_default_selected_option(self):
        '''
        Test that markup for a default selected option when a form is
        instantiated with a salable Product with linked multivariate attributes.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        form = ProductOrderForm(product)

        markup = '<option value="" selected="selected">Choose a foo</option>'

        self.assertInHTML(markup, str(form))


    def test_form_as_div_surrounds_form_controls_with_div_tags(self):
        '''
        Test that markup for each form control is surrounded by a <div> tag.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        form = ProductOrderForm(product)

        markup = form.as_div().replace('\n', '')

        self.assertRegex(markup, '^<div>.*</div>$')


    def test_form_markup_surrounds_form_controls_with_div_tags(self):
        '''
        Test that markup for each form control is surrounded by a <div> tag.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        form = ProductOrderForm(product)

        markup = str(form).replace('\n', '')

        self.assertRegex(markup, '^<div>.*</div>$')


    def test_bound_form_provides_cleaned_data_as_dict_of_sets(self):
        '''
        Test that the cleaned_data property of the form returns a dict of sets.
        '''
        product = Product.objects.create(sku='foo', name='foo')

        request = HttpRequest()
        request.method = 'POST'
        request.POST['foo'] = 'bar'
        form = ProductOrderForm(product, data=request.POST)
        form.full_clean()

        self.assertEqual(form.cleaned_data, {'foo': {'bar'}})
