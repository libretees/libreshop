from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from orders.models import Order, Purchase
from products.models import Product, Variant
from ..views import ConfirmationView, UUID

class ConfirmationViewTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up HTTP request.
        factory = RequestFactory()
        self.request = factory.get(reverse('checkout:confirmation'))

        # Set `session` manually, since middleware is not supported.
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        # Set `user` manually, since middleware is not supported.
        self.request.user = AnonymousUser()

        # Set up test data.
        self.view = ConfirmationView.as_view()


    def test_view_returns_200_status_if_no_order_token_is_in_session_variables(self):
        '''
        Test that the ConfirmationView returns a 200 OK status if there is no
        Order Token within session variables.
        '''
        response = self.view(self.request)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_returns_200_status_if_order_token_is_in_session_variables(self):
        '''
        Test that the ConfirmationView returns a 200 OK status if an Order Token
        is present within session variables.
        '''
        # Set up Product, Variant, Order, and Purchase.
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456'
        )
        order = Order.objects.create()
        purchase = Purchase.objects.create(order=order, variant=variant)

        # Add Order Token to session variables.
        self.request.session[UUID] = {}
        self.request.session[UUID]['order_token'] = order.token
        self.request.session.modified = True

        # Perform test.
        response = self.view(self.request)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)
