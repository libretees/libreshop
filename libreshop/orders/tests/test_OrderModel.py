import logging
from django.test import TestCase
from addresses.models import Address
from products.models import Product, Variant
from ..models import Order, Purchase, Transaction


try:
    # Try to import from the Python 3.3+ standard library.
    from unittest.mock import patch
except ImportError as e:
    # Otherwise, import from the `mock` project dependency.
    from mock import patch

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class OrderModelTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up supplemental test data.
        address = Address.objects.create(
            recipient_name = 'Foo Bar',
            street_address = 'Apt 123\r\nTest St',
            locality = 'Test',
            region = 'OK',
            postal_code = '12345',
            country = 'US'
        )
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456'
        )

        # Set up test data.
        self.order = Order.objects.create(token='foo', shipping_address=address)
        self.purchase = Purchase.objects.create(
            order=self.order, variant=variant
        )
        self.transaction = Transaction.objects.create(
            order=self.order, transaction_id='bar'
        )


    @patch('orders.models.order.randrange')
    def test_model_generates_unique_random_order_token(self, randrange_mock):
        '''
        Test that the orders.Order model generates a unique order token.
        '''
        randrange_mock.return_value = 322424845
        order = Order.objects.create()
        self.assertEqual(order.token, '1337d00d')


    def test_model_handles_conflicting_order_tokens(self):
        '''
        Test that the orders.Order model properly handles conflicting token
        requests.
        '''
        order1 = Order.objects.create(token='1337d00d')
        order2 = Order.objects.create(token='1337d00d')
        self.assertNotEqual(order1.token, order2.token)


    def test_fulfilled_property_provides_false_fulfillment_status_when_incomplete(self):
        '''
        Test that the Order.fulfilled property provides a False value when the
        Order fulfillment status is incomplete.
        '''
        fulfilled = getattr(self.order, 'fulfilled', None)
        self.assertFalse(fulfilled)


    def test_fulfilled_property_provides_true_fulfillment_status_when_complete(self):
        '''
        Test that the Order.fulfilled property provides a True value when the
        Order fulfillment status is complete.
        '''
        self.purchase.fulfilled = True
        self.purchase.save()

        fulfilled = getattr(self.order, 'fulfilled', None)
        self.assertTrue(fulfilled)
