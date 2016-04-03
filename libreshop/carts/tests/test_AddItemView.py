from decimal import Decimal
from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from products.models import Product, Variant
from ..utils import SessionCart
from ..views import AddItemView

# Create your tests here.
class AddItemViewTest(TestCase):

    def setUp(self):
        # Set up test data.
        product = Product.objects.create(name='foo', sku='123')
        self.variant = Variant.objects.create(
            product=product, name='bar', price=Decimal(12.34), sub_sku='456'
        )
        self.variant2 = Variant.objects.create(
            product=product, name='baz', price=Decimal(12.34), sub_sku='789',
            enabled=False
        )

        # Generate a Request object.
        factory = RequestFactory()
        self.request = factory.post(reverse('cart:add'))

        # Set `session` manually, since middleware is not supported.
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        # Set `user` manually, since middleware is not supported.
        self.request.user = AnonymousUser()


    def test_view_issues_redirect_response(self):
        '''
        Test that the AddItemView responds with a HTTP 302 Redirect.
        '''
        view = AddItemView.as_view()
        response = view(self.request)
        self.assertEqual(response.status_code, 302)


    def test_view_redirects_to_site_root_by_default(self):
        '''
        Test that the AddItemView redirects to the site root, by default.
        '''
        view = AddItemView.as_view()
        response = view(self.request)
        self.assertEqual(response.url, '/')


    def test_view_redirects_to_location_in_next_post_variable(self):
        '''
        Test that the AddItemView redirects to the location specified in
        POST['next'], if it is specified.
        '''
        self.request.POST['next'] = 'http://example.com'
        view = AddItemView.as_view()
        response = view(self.request)
        self.assertEqual(response.url, 'http://example.com')


    def test_view_adds_valid_item_to_cart(self):
        '''
        Test that the AddItemView adds a valid item to a SessionCart by SKU.
        '''
        self.request.POST['sku'] = '123456'
        view = AddItemView.as_view()
        response = view(self.request)
        cart = SessionCart(self.request.session)
        self.assertIn(self.variant, cart)


    def test_view_ignores_invalid_skus(self):
        '''
        Test that the AddItemView ignores invalid SKUs.
        '''
        self.request.POST['sku'] = '654321'
        view = AddItemView.as_view()
        response = view(self.request)
        cart = SessionCart(self.request.session)
        self.assertEqual(cart, [])


    def test_view_ignores_invalid_items(self):
        '''
        Test that the AddItemView ignores invalid items.
        '''
        self.request.POST['sku'] = '123789'
        view = AddItemView.as_view()
        response = view(self.request)
        cart = SessionCart(self.request.session)
        self.assertEqual(cart, [])