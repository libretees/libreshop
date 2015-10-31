from importlib import import_module
from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
from .sessioncart import SessionCart

# Create your tests here.
class SessionCartTest(TestCase):

    def test_sessioncart_module_has_uuid(self):
        '''
        Test that SessionCart uses a universally unique identifier (UUID).
        '''
        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)
        self.assertIsNotNone(uuid)


    def test_sessioncart_creates_key_within_session_variable(self):
        '''
        Test that SessionCart creates a key within request.session.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)
        key_created = request.session.has_key(uuid)

        self.assertTrue(key_created)


    def test_sessioncart_maintains_list_within_session_variable(self):
        '''
        Test that SessionCart maintains a list within request.session.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)

        value = request.session.get(uuid)

        self.assertIsInstance(value, list)


    def test_sessioncart_can_add_new_items_to_list(self):
        '''
        Test that SessionCart can add new items to the list in request.session.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)

        before = list(request.session.get(uuid))
        cart.add('foo')
        after = list(request.session.get(uuid))

        self.assertNotEqual(before, after)


    def test_sessioncart_has_session_attribute(self):
        '''
        Test that SessionCart.session is present.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)
        session = getattr(cart, 'session', None)
        self.assertIsNotNone(session)


    def test_sessioncart_has_count_property(self):
        '''
        Test that SessionCart.count is present.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)
        count = getattr(cart, 'count', None)
        self.assertIsNotNone(count)


    def test_sessioncart_increases_count_by_one_after_an_item_is_added(self):
        '''
        Test that SessionCart.count increases by one after a new item is added.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)

        before = cart.count
        cart.add('foo')
        after = cart.count
        delta = after - before

        self.assertEqual(delta, 1)


    def test_sessioncart_has_has_products_property(self):
        '''
        Test that SessionCart.has_products is present.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)
        has_products = getattr(cart, 'has_products', None)
        self.assertIsNotNone(has_products)


    def test_sessioncart_has_products_property_is_false_when_no_items_are_present(self):
        '''
        Test that SessionCart.has_products is False when the SessionCart
        contains no items.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)
        has_products = getattr(cart, 'has_products', None)
        self.assertFalse(has_products)


    def test_sessioncart_has_products_property_is_true_when_items_are_present(self):
        '''
        Test that SessionCart.has_products is True when the SessionCart contains
        items.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        cart = SessionCart(request.session)
        cart.add('foo')
        has_products = getattr(cart, 'has_products', None)
        self.assertTrue(has_products)
