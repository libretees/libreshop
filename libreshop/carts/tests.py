from importlib import import_module
from django.test import TestCase
from .utils import SessionList

# Create your tests here.
class SessionListTest(TestCase):

    def test_sessionlist_module_has_uuid(self):
        '''
        Test that SessionList uses a universally unique identifier (UUID).
        '''
        module = import_module('carts.utils')
        uuid = getattr(module, 'UUID', None)
        self.assertIsNotNone(uuid)


    def test_sessionlist_has_session_attribute(self):
        '''
        Test that SessionList.session is present.
        '''
        session_list = SessionList(self.client.session)
        session = getattr(session_list, 'session', None)
        self.assertIsNotNone(session)


    def test_sessionlist_creates_key_within_session_variable(self):
        '''
        Test that SessionList creates a key within request.session.
        '''
        session = self.client.session
        session_list = SessionList(session)
        module = import_module('carts.utils')
        uuid = getattr(module, 'UUID', None)
        key_created = session.has_key(uuid)
        self.assertTrue(key_created)


    def test_sessionlist_maintains_list_within_session_variable(self):
        '''
        Test that SessionList maintains a list within request.session.
        '''
        session = self.client.session
        session_list = SessionList(session)
        module = import_module('carts.utils')
        uuid = getattr(module, 'UUID', None)
        value = session.get(uuid)
        self.assertIsInstance(value, list)


    def test_sessionlist_does_not_maintain_self_within_session_variable(self):
        '''
        Test that SessionList does not maintain itself within request.session.
        '''
        session = self.client.session
        session_list = SessionList(session)
        module = import_module('carts.utils')
        uuid = getattr(module, 'UUID', None)
        value = session.get(uuid)
        self.assertNotIsInstance(value, SessionList)


    def test_sessionlist_can_be_instantiated_with_a_list(self):
        '''
        Test that SessionList can be instantiated with a list.
        '''
        session = self.client.session
        session_list1 = SessionList(session, ['foo', 'bar'])
        session_list2 = SessionList(session)
        self.assertEqual(session_list2, ['foo', 'bar'])


    def test_sessionlist_can_append_items_to_list(self):
        '''
        Test that SessionList can append items to request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session)
        session_list1.append('foo')
        session_list2 = SessionList(session)
        self.assertEqual(session_list2, ['foo'])


    def test_sessionlist_can_extend_list_with_another_list(self):
        '''
        Test that SessionList can extend request.session with another list.
        '''
        session = self.client.session
        session_list1 = SessionList(session)
        session_list1.extend(['foo', 'bar'])
        session_list2 = SessionList(session)
        self.assertEqual(session_list2, ['foo', 'bar'])


    def test_sessionlist_can_insert_an_item_at_a_given_position(self):
        '''
        Test that SessionList can insert an item to request.session at a given
        position.
        '''
        session = self.client.session
        session_list1 = SessionList(session)
        session_list1.insert(0, 'foo')
        session_list1.insert(1, 'bar')
        session_list2 = SessionList(session)
        self.assertEqual(session_list2, ['foo', 'bar'])


    def test_sessionlist_can_delete_an_item_at_a_given_position(self):
        '''
        Test that SessionList can delete an item from request.session at a given
        position.
        '''
        session = self.client.session
        session_list1 = SessionList(session, ['foo', 'bar'])
        session_list2 = SessionList(session)
        del session_list2[1]
        session_list3 = SessionList(session)
        self.assertEqual(session_list3, ['foo'])


    def test_sessionlist_can_update_an_item_at_a_given_position(self):
        '''
        Test that SessionList can update an item in request.session at a given
        position.
        '''
        session = self.client.session
        session_list1 = SessionList(session, ['foo'])
        session_list1[0] = 'bar'
        session_list2 = SessionList(session)
        self.assertEqual(session_list2, ['bar'])


    def test_sessionlist_can_add_a_list_to_itself(self):
        '''
        Test that SessionList can add a list to request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session)
        session_list1 += ['foo', 'bar']
        session_list2 = SessionList(session)
        self.assertEqual(session_list2, ['foo', 'bar'])


    def test_sessionlist_can_duplicate_itself_by_an_integer_amount(self):
        '''
        Test that SessionList can duplicate itself within request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session, [1])
        session_list1 *= 3
        session_list2 = SessionList(session)
        self.assertEqual(session_list2, [1, 1, 1])


    def test_sessionlist_can_remove_item(self):
        '''
        Test that SessionList can remove an item from request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session, ['foo', 'bar'])
        session_list2 = SessionList(session)
        session_list2.remove('bar')
        session_list3 = SessionList(session)
        self.assertEqual(session_list3, ['foo'])


    def test_sessionlist_pop_removes_item_from_session(self):
        '''
        Test that the SessionList.pop function removes an item from a given
        position in request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session, ['foo', 'bar'])
        session_list2 = SessionList(session)
        session_list2.pop(1)
        session_list3 = SessionList(session)
        self.assertEqual(session_list3, ['foo'])


    def test_sessionlist_pop_returns_item_from_session(self):
        '''
        Test that the SessionList.pop function returns an item from a given
        position in request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session, ['bar', 'foo'])
        session_list2 = SessionList(session)
        val1 = session_list2.pop(1)
        val2 = session_list2.pop(0)
        session_list3 = SessionList(session)
        self.assertEqual([val1, val2], ['foo', 'bar'])


    def test_sessionlist_can_clear_all_items(self):
        '''
        Test that SessionList can clear all items from request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session, ['foo', 'bar'])
        session_list2 = SessionList(session)
        session_list2.clear()
        session_list3 = SessionList(session)
        self.assertEqual(session_list3, [])


    def test_sessionlist_can_sort_items(self):
        '''
        Test that SessionList can sort the items in request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session, [2, 3, 1])
        session_list2 = SessionList(session)
        session_list2.sort()
        session_list3 = SessionList(session)
        self.assertEqual(session_list3, [1, 2, 3])


    def test_sessionlist_can_reverse_items(self):
        '''
        Test that SessionList can reverse the items in request.session.
        '''
        session = self.client.session
        session_list1 = SessionList(session, ['bar', 'foo'])
        session_list2 = SessionList(session)
        session_list2.reverse()
        session_list3 = SessionList(session)
        self.assertEqual(session_list3, ['foo', 'bar'])
