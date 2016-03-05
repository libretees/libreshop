from importlib import import_module
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase, RequestFactory
from carts import SessionList
from products.forms import ProductOrderForm
from products.models import Product, Variant
from ..views import ProductView


class ProductViewTest(TestCase):

    def test_view_displays_correct_title(self):
        '''
        Test that the FormView displays the correct title.
        '''
        product = Product.objects.create(name='foo', sku='1000')

        factory = RequestFactory()
        request = factory.get(
            reverse('products:product', kwargs={'slug': 'foo'})
        )

        # Set `session` manually, since middleware is not supported.
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        # Set `user` manually, since middleware is not supported.
        request.user = AnonymousUser()

        view = ProductView.as_view()
        response = view(request, slug='foo')
        response = response.render()

        self.assertIn(b'<title>LibreShop</title>', response.content)


    def test_view_uses_featured_products_template(self):
        '''
        Test that the FormView uses the products/featured.html template.
        '''
        product = Product.objects.create(name='foo', sku='1000')
        response = self.client.get(
            reverse('products:product', kwargs={'slug': 'foo'})
        )
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
        request.method = 'POST'
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        product_view = ProductView()
        product_view.request = request
        product_view.dispatch(request, slug='foo')
        form = product_view.get_form()
        self.assertIsInstance(form, ProductOrderForm)


    def test_view_adds_variant_id_to_cart_when_form_is_valid(self):
        '''
        Test that a Variant.id is added to a SessionList when valid POST data is
        submitted.
        '''
        product = Product.objects.create(name='foo', sku='1000')

        request = HttpRequest()
        request.method = 'POST'
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        product_view = ProductView()
        product_view.request = request
        product_view.dispatch(request, slug='foo')
        form = product_view.get_form()
        form.full_clean()
        form = product_view.form_valid(form)

        cart = SessionList(request.session)
        variant_id = product.variant_set.first().id

        self.assertIn(variant_id, cart)


    def test_view_context_cart_is_a_list(self):
        '''
        Test that context dict contains a 'cart' key.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        homepage_view = ProductView()
        homepage_view.request = request
        context = homepage_view.get_context_data()

        cart = context.get('cart')

        self.assertIsNotNone(cart)
