from importlib import import_module
from django.http import HttpRequest
from django.conf import settings
from django.test import TestCase
from carts import SessionCart
from products.forms import ProductOrderForm
from products.models import Product, Variant
from ..views import HomepageView


class HomepageViewTest(TestCase):

    def test_view_uses_featured_products_template(self):
        '''
        Test that the view uses the products/featured.html template.
        '''
        product = Product.objects.create(name='foo', sku='1000')
        response = self.client.get('')
        self.assertTemplateUsed(response, 'products/featured.html')


    def test_view_template_includes_csrf_token(self):
        '''
        Test that the view's template includes a CSRF token.
        '''
        product = Product.objects.create(name='foo', sku='1000')
        response = self.client.get('')
        csrf_token_regex = "<input type='hidden' name='csrfmiddlewaretoken' value='[A-Za-z0-9]{32}' />"
        rendered_html = response.content.decode()
        self.assertRegex(rendered_html, csrf_token_regex)


    def test_view_uses_product_order_form(self):
        '''
        Test that the FormView uses the ProductOrderForm Form.
        '''
        product = Product.objects.create(name='foo', sku='1000')

        request = HttpRequest()
        homepage_view = HomepageView()
        homepage_view.request = request
        form = homepage_view.get_form()
        self.assertIsInstance(form, ProductOrderForm)


    def test_view_adds_variant_id_to_cart_when_form_is_valid(self):
        '''
        Test that a Variant.id is added to a SessionCart when valid POST data is
        submitted.
        '''
        product = Product.objects.create(name='foo', sku='1000')

        request = HttpRequest()
        request.method = 'POST'
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        homepage_view = HomepageView()
        homepage_view.request = request
        form = homepage_view.get_form()
        form.full_clean()
        form = homepage_view.form_valid(form)

        cart = SessionCart(request.session)
        variant_id = product.variant_set.first().id

        self.assertIn(variant_id, cart)


    def test_view_context_includes_session_cart(self):
        '''
        Test that the context provided by the FormView includes a SessionCart.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        homepage_view = HomepageView()
        homepage_view.request = request
        context = homepage_view.get_context_data()

        cart = context.get('cart', None)

        self.assertIsInstance(cart, SessionCart)
