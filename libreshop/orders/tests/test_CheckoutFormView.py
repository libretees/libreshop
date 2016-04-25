from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from orders.models import Order, Purchase, Transaction
from products.models import Product, Variant
from ..views import CheckoutFormView, UUID

class CheckoutFormViewTest(TestCase):

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


    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.view = CheckoutFormView.as_view()

        # Set up HTTP request.
        self.create_http_request('GET')


    def test_view_returns_200_status_if_no_variants_are_in_cart(self):
        '''
        Test that the CheckoutFormView returns a 200 OK status if there are no
        Variants within a SessionCart.
        '''
        response = self.view(self.request)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)
