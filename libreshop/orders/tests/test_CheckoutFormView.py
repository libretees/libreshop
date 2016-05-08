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
from .. import views
try:
    # Try to import from the Python 3.3+ standard library.
    from unittest.mock import patch
except ImportError as e:
    # Otherwise, import from the `mock` project dependency.
    from mock import patch


class CheckoutFormViewTest(TestCase):

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

        self.view_url = reverse('checkout:main')


    def test_view_returns_200_status_if_no_variants_are_in_cart(self):
        '''
        Test that the CheckoutFormView returns a 200 OK status if there are no
        Variants within the SessionCart.
        '''
        response = self.client.get(self.view_url)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_returns_200_status_if_variants_are_in_cart(self):
        '''
        Test that the CheckoutFormView returns a 200 OK status if there are
        Variants the SessionCart.
        '''
        cart = SessionCart(self.client.session)
        cart.add(self.variant)

        response = self.client.get(self.view_url)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_initially_redirects_to_self(self):
        '''
        Test that the CheckoutFormView initially redirects to itself.
        '''
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

        response = self.client.post(self.view_url, data=request_data)

        self.assertEqual(response.url, self.view_url)


    @patch('orders.views.calculate_shipping_cost')
    def test_view_advances_to_payment_form(self, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView can advance to the PaymentForm
        '''
        calculate_shipping_cost_mock.return_value = Decimal(1.00)

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

        response = self.client.post(
            self.view_url, data=request_data, follow=True
        )
        rendered_html = response.content.decode()

        self.assertIn('how are you paying?', rendered_html)


    @patch('orders.views.calculate_shipping_cost')
    @patch('orders.forms.braintree.Transaction.sale')
    def test_view_advances_to_confirmation_page(self, sale_mock, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView can advance to the PaymentForm
        '''
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
        response1 = self.client.post(
            self.view_url, data=request_data, follow=True
        )

        request_data = {
            'payment_method_nonce': 'fake-valid-nonce'
        }
        response2 = self.client.post(
            self.view_url, data=request_data, follow=True
        )
        rendered_html = response2.content.decode()

        order = Order.objects.last()
        expected = (
            '<h2>Order <strong>%s</strong> has been received!</h2>' %
            order.token
        )

        self.assertIn(expected, rendered_html)


    @patch('orders.views.calculate_shipping_cost')
    def test_view_adds_valid_shipping_information_to_session_variable(self, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView adds valid shipping information from the
        AddressForm to the User's Session.
        '''
        calculate_shipping_cost_mock.return_value = Decimal(1.00)

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
        response = self.client.post(
            self.view_url,
            data=request_data,
            follow=True
        )

        self.assertEqual(
            self.client.session[views.UUID]['shipping'], request_data
        )


    @patch('django.core.mail.backends.locmem.EmailBackend')
    def test_view_can_load_and_retrieve_shipping_cost_from_valid_backend(self, shipping_api_mock):
        '''
        Test that the CheckoutFormView can successfully load and retrieve a
        shipping cost from an API.
        '''
        settings.SHIPPING_APIS = (
            'django.core.mail.backends.locmem.EmailBackend',
        )
        shipping_api_mock.return_value = Decimal(1.00)

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

        response = self.client.post(
            self.view_url,
            data=request_data,
            follow=True
        )

        self.assertEqual(
            self.client.session[views.UUID]['shipping'], request_data
        )


    @patch.object(views, 'settings')
    def test_view_can_load_and_retrieve_shipping_cost_from_invalid_backend(self, settings_mock):
        '''
        Test that the CheckoutFormView can successfully load and retrieve a
        shipping cost from an API.
        '''
        settings_mock.SHIPPING_APIS = (
            'foo',
        )

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

        response = self.client.post(
            self.view_url,
            data=request_data,
            follow=True
        )

        self.assertNotIn(
            'shipping', self.client.session[views.UUID]
        )


    @patch.object(views, 'settings')
    def test_view_can_load_and_retrieve_shipping_cost_from_invalid_backend_attribute(self, settings_mock):
        '''
        Test that the CheckoutFormView can successfully load and retrieve a
        shipping cost from an API.
        '''
        settings_mock.SHIPPING_APIS = (
            'django.core.mail.backends.locmem.foo',
        )

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

        shipping_api = settings.SHIPPING_APIS[0]
        with patch(shipping_api) as shipping_api_mock:
            shipping_api_mock.return_value = Decimal(1.00)

            response = self.client.post(
                self.view_url,
                data=request_data,
                follow=True
            )

        self.assertNotIn(
            'shipping', self.client.session[views.UUID]
        )


    @patch('orders.views.calculate_shipping_cost')
    def test_view_removes_step_data_for_key_in_get_request(self, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView can remove a given key from checkout
        Session Data when it is specified in an HTTP GET request.
        '''
        calculate_shipping_cost_mock.return_value = Decimal(1.00)

        cart = SessionCart(self.client.session)
        cart.add(self.variant)

        request_data = {
            'recipient_name': 'Foo Bar',
            'street_address': '123 Test St',
            'locality': 'Test',
            'region': 'OK',
            'postal_code': '12345',
            'country': 'US'
        }
        response = self.client.post(
            self.view_url, data=request_data, follow=True
        )

        request_data = {
            'shipping': 'shipping'
        }
        response = self.client.get(self.view_url, data=request_data)

        self.assertNotIn('shipping', self.client.session[views.UUID])


    @patch('orders.views.calculate_shipping_cost')
    def test_view_gracefully_handles_invalid_step_data_deletion_requests(self, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView gracefully handles step deletion when the
        step is not present within checkout Session Data.
        '''
        calculate_shipping_cost_mock.return_value = Decimal(1.00)

        cart = SessionCart(self.client.session)
        cart.add(self.variant)

        # Set up HTTP GET request.
        request_data = {
            'shipping': 'shipping'
        }
        response = self.client.get(self.view_url, data=request_data)

        self.assertNotIn('shipping', self.client.session[views.UUID])
