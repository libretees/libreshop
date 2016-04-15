from django.contrib.admin import site
from django.http import HttpRequest
from django.test import TestCase
from addresses.models import Address
from products.models import Product, Variant
from ..admin import OrderAdmin
from ..models import Order, Purchase, Transaction

# Create your tests here.
class OrderAdminTest(TestCase):

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
        order = Order.objects.create(token='foo', shipping_address=address)
        self.purchase = Purchase.objects.create(
            order=order, variant=variant
        )
        self.transaction = Transaction.objects.create(
            order=order, transaction_id='bar'
        )

        # Set up basic test.
        self.request = HttpRequest()
        self.admin = OrderAdmin(Order, site)
        self.order = self.admin.get_object(self.request, order.pk)


    def test_fulfilled_list_display_matches_order_fulfillment_status(self):
        '''
        Test that the result given by the OrderAdmin._fulfilled method is the
        same as the result provided by the Order.fulfilled property.
        '''
        result = None
        method = getattr(self.admin, '_fulfilled', None)
        if method:
            result = method(self.order)

        self.assertEqual(result, self.order.fulfilled)


    def test_fulfilled_purchases_list_display_matches_number_of_fulfilled_purchases(self):
        '''
        Test that the result given by the OrderAdmin._fulfilled_purchases method
        is equal to the number of fulfilled Purchases under the Order.
        '''
        self.purchase.fulfilled = True
        self.purchase.save()

        order = self.admin.get_object(self.request, self.order.pk)

        result = None
        method = getattr(self.admin, '_fulfilled_purchases', None)
        if method:
            result = method(order)

        self.assertEqual(result, 1)


    def test_purchases_list_display_matches_number_of_purchases(self):
        '''
        Test that the result given by the OrderAdmin._purchases method is equal
        to the number of Purchases under the Order.
        '''
        result = None
        method = getattr(self.admin, '_purchases', None)
        if method:
            result = method(self.order)

        self.assertEqual(result, 1)


    def test_recipient_list_display_shows_order_recipient_name(self):
        '''
        Test that the result given by the OrderAdmin._recipient method returns
        the name of the Order recipient.
        '''
        result = None
        method = getattr(self.admin, '_recipient', None)
        if method:
            result = method(self.order)

        self.assertEqual(result, self.order.shipping_address.recipient_name)
