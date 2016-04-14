import string
import random
import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from addresses.models import Address
from ..models import Warehouse

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class WarehouseModelTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.address = Address.objects.create()
        self.warehouse = Warehouse.objects.create(
            name='foo', address=self.address
        )


    def test_model_string_representation(self):
        '''
        Test that the Warehouse string representation displays properly.
        '''
        self.assertEqual(str(self.warehouse), 'Warehouse foo')


    def test_model_has_name_field(self):
        '''
        Test that Warehouse.name is present.
        '''
        name = getattr(self.warehouse, 'name', None)
        self.assertIsNotNone(name)


    def test_model_has_address_field(self):
        '''
        Test that Warehouse.address is present.
        '''
        address = getattr(self.warehouse, 'address', None)
        self.assertIsNotNone(address)


    def test_saving_to_and_retrieving_warehouses_from_the_database(self):
        '''
        Test that a Warehouse can be successfuly saved to the database.
        '''
        warehouse = Warehouse(name='bar', address=Address.objects.create())
        warehouse.save()
        num_warehouses = Warehouse.objects.filter(name='bar').count()
        self.assertEqual(num_warehouses, 1)


    def test_name_field_is_required(self):
        '''
        Test that Warehouse.name is required.
        '''
        func = Warehouse.objects.create
        self.assertRaises(
            IntegrityError, func, name=None, address=Address.objects.create()
        )


    def test_address_field_is_required(self):
        '''
        Test that Warehouse.address is required.
        '''
        func = Warehouse.objects.create
        self.assertRaises(ValueError, func, name='bar', address=None)


    def test_name_field_must_be_unique(self):
        '''
        Test that Warehouse.name must be unique.
        '''
        func = Warehouse.objects.create
        self.assertRaises(
            ValidationError, func, name='foo', address=Address.objects.create()
        )


    def test_name_field_can_be_updated_to_different_character_case(self):
        '''
        Test that a model instance can update the character case of its own
        unique name.
        '''
        self.warehouse.name = 'FOO'
        self.warehouse.save()
        self.assertEqual(self.warehouse.name, 'FOO')


    def test_name_field_must_be_unique_regardless_of_character_case(self):
        '''
        Test that Warehouse.name must be unique regardless of character case.
        '''
        func = Warehouse.objects.create
        self.assertRaises(
            ValidationError, func, name='Foo', address=Address.objects.create()
        )


    def test_name_and_address_field_must_be_unique_together(self):
        '''
        Test that Warehouse.name and Warehouse.address must be unique together.
        '''
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='foo', address=self.address)


    def test_address_field_must_be_unique(self):
        '''
        Test that Warehouse.address must be unique.
        '''
        func = Warehouse.objects.create
        self.assertRaises(
            ValidationError, func, name='bar', address=self.address
        )


    def test_name_field_is_correct_length(self):
        '''
        Test that Warehouse.name must be less than or equal to 64 characters in
        length.

        Note that sqlite does not enforce VARCHAR field length constraints.
        '''
        max_length = 64
        database_engine = settings.DATABASES['default']['ENGINE']
        random_string = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(max_length+1)
        )
        if database_engine != 'django.db.backends.sqlite3':
            func = Warehouse.objects.create
            self.assertRaises(
                IntegrityError, func, name=random_string, address=self.address
            )
