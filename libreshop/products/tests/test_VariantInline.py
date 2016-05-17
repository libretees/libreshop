from django.contrib.admin import site
from django.http import HttpRequest
from django.test import TestCase
from ..admin import VariantInline
from ..models import Product

# Create your tests here.
class VariantInlineTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.product = Product.objects.create(name='foo', sku='foo')


    def test_max_num_equal_to_number_of_child_objects(self):
        '''
        Test that the maximum number of Variant objects listed in the
        InlineModelAdmin is equal to the number of children to the parent
        Product.
        '''
        request = HttpRequest()
        admin = VariantInline(Product, site)

        max_num = admin.get_max_num(request, obj=self.product)

        self.assertEqual(max_num, 1)
