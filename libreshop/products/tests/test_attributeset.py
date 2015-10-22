import logging
from django.test import TestCase
from ..utils import AttributeSet

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class AttriubteSetTest(TestCase):

    def test_empty_attribute_set_is_represented_as_set(self):
        '''
        Test that an empty AttributeSet is represented the same as a Python set.
        '''
        attribute_set = AttributeSet()
        set_ = {}
        self.assertEqual(repr(attribute_set), repr(set_))


    def test_populated_attribute_set_is_represented_as_set(self):
        '''
        Test that a populated AttributeSet is represented the same as a Python set.
        '''
        attribute_set = AttributeSet({'foo', 'bar'})
        set_ = {'foo', 'bar'}
        self.assertEqual(repr(attribute_set), repr(set_))
