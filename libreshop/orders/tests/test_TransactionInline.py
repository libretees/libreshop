from django.contrib.admin import site
from django.http import HttpRequest
from django.test import TestCase
from products.models import Product, Variant
from ..admin import TransactionInline
from ..models import Order, Purchase, Transaction

# Create your tests here.
class TransactionInlineInlineTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.order = Order.objects.create(token='foo')

        # Set up supplemental test data.
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456'
        )
        purchase = Purchase.objects.create(order=self.order, variant=variant)
        transaction = Transaction.objects.create(
            order=self.order, transaction_id='bar'
        )


    def test_max_num_equal_to_number_of_child_objects(self):
        '''
        Test that the maximum number of Transaction objects listed in the
        InlineModelAdmin is equal to the number of children to the parent
        Order.
        '''
        request = HttpRequest()
        admin = TransactionInline(Order, site)

        max_num = admin.get_max_num(request, obj=self.order)

        self.assertEqual(max_num, 1)
