from decimal import Decimal
from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.utils import timezone
from orders.models import Order, Purchase, Transaction
from carts.utils import SessionCart
from orders.models import Order
from products.models import Product, Variant
from ..views import CheckoutFormView, UUID
try:
    # Try to import from the Python 3.3+ standard library.
    from unittest.mock import patch
except ImportError as e:
    # Otherwise, import from the `mock` project dependency.
    from mock import patch


class CheckoutFormViewTest(TestCase):

    def create_http_request(self, method, data=None):
        '''
        Create an HTTP request based on the `method` parameter. Any data that is
        to be passed along with the request should come in dict form with the
        `data` parameter.
        '''
        factory = RequestFactory()

        http_method = getattr(factory, method.lower())
        self.request = http_method(reverse('checkout:main'), data=data)

        # Set `user` manually, since middleware is not supported.
        self.request.user = AnonymousUser()

        # Set `session` manually, since middleware is not supported.
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        self.request.session = engine.SessionStore(session_key)


    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        product = Product.objects.create(name='foo', sku='123')
        variant = product.variant_set.first()
        variant.price = Decimal(12.34)
        variant.sub_sku = '456'
        variant.save()
        self.variant = variant
        self.variant2 = Variant.objects.create(
            product=product, name='bar', price=Decimal(43.21), sub_sku='789'
        )

        self.view = CheckoutFormView.as_view()

        # Set up HTTP request.
        self.create_http_request('GET')


    def test_view_returns_200_status_if_no_variants_are_in_cart(self):
        '''
        Test that the CheckoutFormView returns a 200 OK status if there are no
        Variants within the SessionCart.
        '''
        response = self.view(self.request)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_returns_200_status_if_variants_are_in_cart(self):
        '''
        Test that the CheckoutFormView returns a 200 OK status if there are
        Variants the SessionCart.
        '''
        cart = SessionCart(self.request.session)
        cart.add(self.variant)

        response = self.view(self.request)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_initially_redirects_to_self(self):
        '''
        Test that the CheckoutFormView initially redirects to itself.
        '''
        view_url = reverse('checkout:main')

        cart = SessionCart(self.client.session)
        cart.add(self.variant)

        # Set up HTTP POST request.
        request_data = {
            'recipient_name': 'Foo Bar',
            'street_address': '123 Test St',
            'locality': 'Test',
            'region': 'OK',
            'postal_code': '12345',
            'country': 'US'
        }

        response = self.client.post(view_url, data=request_data)

        self.assertEqual(response.url, view_url)


    @patch('orders.views.calculate_shipping_cost')
    def test_view_advances_to_payment_form(self, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView can advance to the PaymentForm
        '''
        view_url = reverse('checkout:main')

        cart = SessionCart(self.client.session)
        cart.add(self.variant)

        calculate_shipping_cost_mock.return_value = Decimal(1.00)

        # Set up HTTP POST request.
        request_data = {
            'recipient_name': 'Foo Bar',
            'street_address': '123 Test St',
            'locality': 'Test',
            'region': 'OK',
            'postal_code': '12345',
            'country': 'US'
        }

        response = self.client.post(view_url, data=request_data, follow=True)
        rendered_html = response.content.decode()

        self.assertIn('how are you paying?', rendered_html)


    @patch('orders.views.calculate_shipping_cost')
    @patch('orders.forms.braintree.Transaction.sale')
    def test_view_advances_to_confirmation_page(self, sale_mock, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView can advance to the PaymentForm
        '''
        view_url = reverse('checkout:main')

        cart = SessionCart(self.client.session)
        cart.add(self.variant)

        calculate_shipping_cost_mock.return_value = Decimal(1.00)

        sale_mock.return_value.is_success = True
        sale_mock.return_value.transaction.id = '12345'
        sale_mock.return_value.transaction.amount = Decimal(1.00)
        sale_mock.return_value.transaction.created_at = timezone.now()
        sale_mock.return_value.transaction.credit_card = {
            'cardholder_name': 'Foo Bar',
            'customer_location': 'US',
            'card_type': 'Foo',
            'last_4': '1234',
            'expiration_month': '12',
            'expiration_year': '2034',
        }

        # Set up HTTP POST request.
        request_data = {
            'recipient_name': 'Foo Bar',
            'street_address': '123 Test St',
            'locality': 'Test',
            'region': 'OK',
            'postal_code': '12345',
            'country': 'US'
        }

        response1 = self.client.post(view_url, data=request_data, follow=True)

        request_data = {
            'payment_method_nonce': 'fake-valid-nonce'
        }

        response2 = self.client.post(view_url, data=request_data, follow=True)
        rendered_html = response2.content.decode()

        order = Order.objects.last()
        expected = (
            '<h2>Order <strong>%s</strong> has been received!</h2>' %
            order.token
        )

        self.assertIn(expected, rendered_html)
