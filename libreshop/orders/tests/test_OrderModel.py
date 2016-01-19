import logging
from django.test import TestCase
from .. import models

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

    @patch.object(models, 'randrange')
    def test_model_generates_unique_random_order_token(self, randrange_mock):
        '''
        Test that the orders.Order model generates a unique order token.
        '''
        randrange_mock.return_value = 322424845
        order = models.Order.objects.create()
        self.assertEqual(order.token, '1337d00d')


    def test_model_handles_conflicting_order_tokens(self):
        '''
        Test that the orders.Order model properly handles conflicting token
        requests.
        '''
        order1 = models.Order.objects.create(token='1337d00d')
        order2 = models.Order.objects.create(token='1337d00d')
        self.assertNotEqual(order1.token, order2.token)
