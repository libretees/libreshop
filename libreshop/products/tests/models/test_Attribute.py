import logging
import random
import string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from ...models import Attribute

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class AttributeModelTest(TestCase):

    def test_model_has_name_field(self):
        '''
        Test that Attribute.name is present.
        '''
        attribute = Attribute.objects.create(name='foo')
        name = getattr(attribute, 'name', None)
        self.assertIsNotNone(name)


    def test_saving_to_and_retrieving_attributes_from_the_database(self):
        '''
        Test that an Attribute can be successfuly saved to the database.
        '''
        attribute = Attribute(name='foo')
        attribute.save()
        num_attributes = Attribute.objects.all().count()
        self.assertEqual(num_attributes, 1)


    def test_name_field_is_required(self):
        '''
        Test that Attribute.name is required.
        '''
        func = Attribute.objects.create
        self.assertRaises(IntegrityError, func, name=None)


    def test_name_field_must_be_unique(self):
        '''
        Test that Attribute.name must be unique.
        '''
        attribute = Attribute.objects.create(name='foo')
        func = Attribute.objects.create
        self.assertRaises(ValidationError, func, name='foo')


    def test_name_field_must_be_unique_regardless_of_character_case(self):
        '''
        Test that Attribute.name must be unique regardless of character case.
        '''
        attribute = Attribute.objects.create(name='foo')
        func = Attribute.objects.create
        self.assertRaises(ValidationError, func, name='Foo')


    def test_name_field_is_correct_length(self):
        '''
        Test that Attribute.name must be less than or equal to 64 characters in
        length.

        Note that sqlite does not enforce VARCHAR field length constraints.
        '''
        max_length = 64
        database_engine = settings.DATABASES['default']['ENGINE']
        random_string = (
            ''.join(
                random.choice(string.ascii_letters + string.digits)
                for _ in range(max_length+1)
            )
        )
        if database_engine != 'django.db.backends.sqlite3':
            func = Attribute.objects.create
            self.assertRaises(IntegrityError, func, name=random_string)
