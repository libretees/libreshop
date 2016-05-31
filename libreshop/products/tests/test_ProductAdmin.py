from django.contrib.admin import site
from django.http import HttpRequest
from django.test import TestCase
from ..admin import ProductAdmin
from ..models import Product

# Create your tests here.
class ProductAdminTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up supplemental test data.
        product = Product.objects.create(sku='foo', name='foo')

        # Set up basic test.
        self.request = HttpRequest()
        self.admin = ProductAdmin(Product, site)
        self.product = self.admin.get_object(self.request, product.pk)
