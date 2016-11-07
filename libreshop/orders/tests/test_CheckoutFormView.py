import logging
from decimal import Decimal
from importlib import import_module
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.utils import timezone
from orders.models import Order, Purchase, Transaction
from carts.utils import SessionCart
from orders.models import Order, TaxRate
from products.models import Product, Variant
from .. import views
try:
    # Try to import from the Python 3.3+ standard library.
    from unittest.mock import patch
except ImportError as e:
    # Otherwise, import from the `mock` project dependency.
    from mock import patch

# Map the Python 2 `__builtin__` module to the Python 3 equivalent.
try:
    import __builtin__ as builtins
except ImportError as e:
    import builtins

# Initialize logger.
logger = logging.getLogger(__name__)

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
        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

        response = self.client.get(self.view_url)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_initially_redirects_to_self(self):
        '''
        Test that the CheckoutFormView initially redirects to itself.
        '''
        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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


    @patch('orders.views.calculate_shipping_cost')
    def test_view_detects_malformed_session_data(self, calculate_shipping_cost_mock):
        '''
        Test that the View validates Session Data on an ongoing basis.
        '''
        calculate_shipping_cost_mock.return_value = Decimal(1.00)

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

        # Set up HTTP POST request.
        session_data = {
            'recipient_name': 'Foo Bar',
            'street_address': '123 Test St',
            'locality': 'Test',
            'region': 'OK',
            'postal_code': '1234567890', # Simulate bad ZIP code.
            'country': 'US'
        }

        session = self.client.session
        session[views.UUID] = {'shipping': session_data}
        session.save()

        request_data = {
            'payment_method_nonce': 'fake-valid-nonce'
        }
        response = self.client.post(
            self.view_url, data=request_data, follow=True
        )
        rendered_html = response.content.decode()

        self.assertNotIn('shipping', self.client.session[views.UUID])


    @patch.object(builtins, 'sum')
    @patch.object(views, 'settings')
    @patch('django.core.mail.backends.locmem.EmailBackend')
    @patch('orders.views.get_shipping_rate')
    def test_view_can_load_and_retrieve_shipping_cost_from_valid_backend(
        self, sum_mock, settings_mock, shipping_api_mock, get_shipping_rate_mock):
        '''
        Test that the CheckoutFormView can successfully load and retrieve a
        shipping cost from an API.
        '''
        settings_mock.FULFILLMENT_BACKENDS = [(
            'django.core.mail.backends.locmem.EmailBackend', 'Foo')]
        shipping_api_mock.return_value = Decimal(1.00)

        sum_mock.return_value = Decimal(0.00)
        get_shipping_rate_mock.return_value = Decimal(1.00)

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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


    @patch.object(builtins, 'sum')
    @patch.object(views, 'settings')
    @patch('orders.views.get_shipping_rate')
    def test_view_can_load_and_retrieve_shipping_cost_from_invalid_backend(
        self, sum_mock, settings_mock, get_shipping_rate_mock):
        '''
        Test that the CheckoutFormView can successfully load and retrieve a
        shipping cost from an API.
        '''
        sum_mock.return_value = Decimal(0.00)
        get_shipping_rate_mock.return_value = Decimal(0.00)

        settings_mock.FULFILLMENT_BACKENDS = [('foo', 'Foo')]

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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


    @patch.object(builtins, 'sum')
    @patch.object(views, 'settings')
    @patch('orders.views.get_shipping_rate')
    def test_view_can_load_and_retrieve_shipping_cost_from_invalid_backend_attribute(self, sum_mock, settings_mock, get_shipping_rate_mock):
        '''
        Test that the CheckoutFormView can recover from a badly-formed package
        import or missing module.
        '''
        sum_mock.return_value = Decimal(0.00)
        get_shipping_rate_mock.return_value = Decimal(0.00)

        settings_mock.FULFILLMENT_BACKENDS = [(
            'django.core.mail.backends.locmem.foo', 'Foo')]

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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


    @patch('orders.views.calculate_shipping_cost')
    def test_view_removes_step_data_for_key_in_get_request(self, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView can remove a given key from checkout
        Session Data when it is specified in an HTTP GET request.
        '''
        calculate_shipping_cost_mock.return_value = Decimal(1.00)

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

        # Set up HTTP GET request.
        request_data = {
            'shipping': 'shipping'
        }
        response = self.client.get(self.view_url, data=request_data)

        self.assertNotIn('shipping', self.client.session[views.UUID])


    @patch('orders.views.calculate_shipping_cost')
    def test_view_calculates_sales_tax_if_nexus_exists(self, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView calculates sales tax when the User
        resides within the nexus of the seller.
        '''
        calculate_shipping_cost_mock.return_value = Decimal(1.00)

        rate = TaxRate.objects.create(
            city='Test', state='OK', postal_code='12345',
            local_tax_rate=Decimal(0.01), state_tax_rate=Decimal(0.043)
        )

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

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
        response = response.render()
        rendered_html = response.content.decode()

        self.assertIn('sales tax', rendered_html)


    @patch('orders.views.calculate_shipping_cost')
    def test_view_d0es_not_calculate_sales_tax_if_no_nexus_exists(self, calculate_shipping_cost_mock):
        '''
        Test that the CheckoutFormView calculates sales tax when the User
        does not reside within the nexus of the seller.
        '''
        calculate_shipping_cost_mock.return_value = Decimal(1.00)

        rate = TaxRate.objects.create(
            city='Test', state='OK', postal_code='12345',
            local_tax_rate=Decimal(0.01), state_tax_rate=Decimal(0.043)
        )

        session = self.client.session
        cart = SessionCart(session)
        cart.add(self.variant)
        session.save()

        # Set up HTTP POST request.
        request_data = {
            'street_address': 'Buckingham Palace',
            'locality': 'London',
            'postal_code': 'SW1A 1AA',
            'country': 'GB'
        }
        response = self.client.post(
            self.view_url,
            data=request_data,
            follow=True
        )
        response = response.render()
        rendered_html = response.content.decode()

        self.assertNotIn('sales tax', rendered_html)


    @patch('orders.views.get_real_ip')
    @patch('orders.views.GeoIP2.country')
    def test_unbound_form_defaults_to_users_country_if_ip_found(
        self, country_mock, get_real_ip_mock):
        '''
        Test that the view geolocates the user's country when a valid IP is
        returned by the `django-ipware` package.
        '''
        get_real_ip_mock.return_value = '127.0.0.1'
        country_mock.return_value = {
            'country_name': 'United States', 'country_code': 'US'
        }

        response = self.client.get(self.view_url)
        response = response.render()
        rendered_html = response.content.decode()

        selected_option = (
            '<option value="US" selected="selected">'
                'United States of America'
            '</option>'
        )
        self.assertIn(selected_option, rendered_html)
