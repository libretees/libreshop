import logging
from django.test import TestCase
from ..utils import AttributeDict

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class AttriubteDictTest(TestCase):

    def test_empty_attribute_dict_is_represented_as_dict(self):
        '''
        Test that an empty AttriubteDict is represented the same as a Python dict.
        '''
        attribute_dict = AttributeDict()
        dict_ = dict()
        self.assertEqual(repr(attribute_dict), repr(dict_))


    def test_attribute_dict_raises_attribute_error_when_non_existent_key_is_accessed(self):
        '''
        Test that an AttriubteDict raises AttributeError when a non-existent key
        is accessed as an attribute.
        '''
        attribute_dict = AttributeDict()
        self.assertRaises(AttributeError, getattr, attribute_dict, 'foo')


    def test_attribute_dict_allows_keys_to_be_accessed_as_attributes(self):
        '''
        Test that an AttriubteDict allows keys to be accessed as attributes.
        '''
        attribute_dict = AttributeDict()
        attribute_dict['foo'] = 'bar'
        value = getattr(attribute_dict, 'foo', None)
        self.assertEqual(attribute_dict['foo'], value)
