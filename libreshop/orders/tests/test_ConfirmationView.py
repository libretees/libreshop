from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from orders.models import Order, Purchase, Transaction
from products.models import Product, Variant
from ..views import ConfirmationView, UUID

class ConfirmationViewTest(TestCase):

    def create_http_request(self, method, data=None):
        '''
        Create an HTTP request based on the `method` parameter. Any data that is
        to be passed along with the request should come in dict form with the
        `data` parameter.
        '''
        factory = RequestFactory()

        http_method = getattr(factory, method.lower())
        self.request = http_method(reverse('checkout:confirmation'), data=data)

        # Set `user` manually, since middleware is not supported.
        self.request.user = AnonymousUser()

        # Set `session` manually, since middleware is not supported.
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        # Add Order Token to session variables.
        self.request.session[UUID] = {}
        self.request.session[UUID]['order_token'] = self.order.token
        self.request.session.modified = True


    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.product = Product.objects.create(name='foo', sku='123')
        self.variant = Variant.objects.create(
            product=self.product, name='bar', sub_sku='456'
        )
        self.order = Order.objects.create()
        self.purchase = Purchase.objects.create(
            order=self.order, variant=self.variant
        )
        self.transaction = Transaction.objects.create(
            order=self.order, transaction_id='foo'
        )
        self.view = ConfirmationView.as_view()

        # Set up HTTP request.
        self.create_http_request('GET')



    def test_view_returns_200_status_if_no_order_token_is_in_session_variables(self):
        '''
        Test that the ConfirmationView returns a 200 OK status if there is no
        Order Token within session variables.
        '''
        # Delete session variable.
        del self.request.session[UUID]['order_token']

        response = self.view(self.request)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_returns_200_status_if_order_token_is_in_session_variables(self):
        '''
        Test that the ConfirmationView returns a 200 OK status if an Order Token
        is present within session variables.
        '''
        # Perform test.
        response = self.view(self.request)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_redirects_on_successful_post(self):
        '''
        Test that the ConfirmationView returns a 302 Found (Temporary Redirect)
        status if valid Form data is POSTed to the View's OrderReceiptForm.
        '''
        # Set up HTTP POST request.
        data = {'email_address': 'test@example.com'}
        self.create_http_request('POST', data=data)

        # Perform test.
        response = self.view(self.request, **data)

        self.assertEqual(response.status_code, 302)
