from django.test import TestCase
from .models import Product

# Create your tests here.
class ProductModelTest(TestCase):

    def test_saving_and_retrieving_products_from_the_database(self):
        product = Product(sku='test', name='test')
        product.save()
        num_products = Product.objects.all().count()

        self.assertEqual(num_products, 1)
