from importlib import import_module
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
        session = self.client.session
        cart = SessionCart(session)

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)
        key_created = session.has_key(uuid)

        self.assertTrue(key_created)


    def test_sessioncart_maintains_list_within_session_variable(self):
        '''
        Test that SessionCart maintains a list within request.session.
        '''
        session = self.client.session
        cart = SessionCart(session)

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)
        value = session.get(uuid)

        self.assertIsInstance(value, list)


    def test_sessioncart_maintains_list_within_session_variable_after_add(self):
        '''
        Test that SessionCart maintains a list within request.session after add.
        '''
        session = self.client.session
        cart = SessionCart(session)
        cart.add('foo')

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)
        value = session.get(uuid)

        self.assertIsInstance(value, list)


    def test_sessioncart_maintains_list_within_session_variable_after_append(self):
        '''
        Test that SessionCart maintains a list within request.session.
        '''
        session = self.client.session
        cart = SessionCart(session)
        cart.append('foo')

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)
        value = session.get(uuid)

        self.assertIsInstance(value, list)


    def test_sessioncart_does_not_maintain_self_within_session_variable(self):
        '''
        Test that SessionCart does not maintain itself within request.session.
        '''
        session = self.client.session
        cart = SessionCart(session)

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)

        value = session.get(uuid)

        self.assertNotIsInstance(value, SessionCart)


    def test_sessioncart_does_not_maintain_self_within_session_variable_after_add(self):
        '''
        Test that SessionCart does not maintain itself within request.session
        after an item has been added.
        '''
        session = self.client.session
        cart = SessionCart(session)
        cart.add('foo')

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)

        value = session.get(uuid)

        self.assertNotIsInstance(value, SessionCart)


    def test_sessioncart_does_not_maintain_self_within_session_variable_after_append(self):
        '''
        Test that SessionCart does not maintain itself within request.session
        after an item has been appended.
        '''
        session = self.client.session
        cart = SessionCart(session)
        cart.append('foo')

        module = import_module('carts.sessioncart')
        uuid = getattr(module, 'UUID', None)

        value = session.get(uuid)

        self.assertNotIsInstance(value, SessionCart)


    def test_sessioncart_maintains_same_list_between_subsequent_instantiations(self):
        '''
        Test that SessionCart maintains the same list between subsequent
        instantiations.
        '''
        session = self.client.session
        cart1 = SessionCart(session)
        cart1.add('foo')
        cart2 = SessionCart(session)

        self.assertEqual(cart2, ['foo'])


    def test_sessioncart_can_add_new_items_to_list(self):
        '''
        Test that SessionCart can add new items to the list in request.session.
        '''
        cart = SessionCart(self.client.session)
        before = cart.copy()
        cart.add('foo')
        after = cart.copy()

        self.assertNotEqual(before, after)


    def test_sessioncart_has_session_attribute(self):
        '''
        Test that SessionCart.session is present.
        '''
        cart = SessionCart(self.client.session)
        session = getattr(cart, 'session', None)
        self.assertIsNotNone(session)


    def test_sessioncart_has_has_products_property(self):
        '''
        Test that SessionCart.has_products is present.
        '''
        cart = SessionCart(self.client.session)
        has_products = getattr(cart, 'has_products', None)
        self.assertIsNotNone(has_products)


    def test_sessioncart_has_products_property_is_false_when_no_items_are_present(self):
        '''
        Test that SessionCart.has_products is False when the SessionCart
        contains no items.
        '''
        cart = SessionCart(self.client.session)
        has_products = getattr(cart, 'has_products', None)
        self.assertFalse(has_products)


    def test_sessioncart_has_products_property_is_true_when_items_are_present(self):
        '''
        Test that SessionCart.has_products is True when the SessionCart contains
        items.
        '''
        cart = SessionCart(self.client.session)
        cart.add('foo')
        has_products = getattr(cart, 'has_products', None)
        self.assertTrue(has_products)
