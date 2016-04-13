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

    def test_model_has_name_field(self):
        '''
        Test that Warehouse.name is present.
        '''
        warehouse = Warehouse.objects.create(name='foo',
            address=Address.objects.create())
        name = getattr(warehouse, 'name', None)
        self.assertIsNotNone(name)


    def test_model_has_address_field(self):
        '''
        Test that Warehouse.address is present.
        '''
        warehouse = Warehouse.objects.create(name='foo',
            address=Address.objects.create())
        address = getattr(warehouse, 'address', None)
        self.assertIsNotNone(address)


    def test_saving_to_and_retrieving_warehouses_from_the_database(self):
        '''
        Test that a Warehouse can be successfuly saved to the database.
        '''
        warehouse = Warehouse(name='foo', address=Address.objects.create())
        warehouse.save()
        num_warehouses = Warehouse.objects.all().count()
        self.assertEqual(num_warehouses, 1)


    def test_name_field_is_required(self):
        '''
        Test that Warehouse.name is required.
        '''
        func = Warehouse.objects.create
        self.assertRaises(IntegrityError, func, name=None,
            address=Address.objects.create())


    def test_address_field_is_required(self):
        '''
        Test that Warehouse.address is required.
        '''
        func = Warehouse.objects.create
        self.assertRaises(ValueError, func, name='foo', address=None)


    def test_name_field_must_be_unique(self):
        '''
        Test that Warehouse.name must be unique.
        '''
        warehouse = Warehouse.objects.create(name='foo',
            address=Address.objects.create())
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='foo',
            address=Address.objects.create())


    def test_name_field_must_be_unique_regardless_of_character_case(self):
        '''
        Test that Warehouse.name must be unique regardless of character case.
        '''
        warehouse = Warehouse.objects.create(name='foo',
            address=Address.objects.create())
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='Foo',
            address=Address.objects.create())


    def test_name_and_address_field_must_be_unique_together(self):
        '''
        Test that Warehouse.name and Warehouse.address must be unique together.
        '''
        address = Address.objects.create()
        warehouse = Warehouse.objects.create(name='foo', address=address)
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='foo', address=address)


    def test_address_field_must_be_unique(self):
        '''
        Test that Warehouse.address must be unique.
        '''
        address = Address.objects.create()
        warehouse = Warehouse.objects.create(name='foo', address=address)
        func = Warehouse.objects.create
        self.assertRaises(ValidationError, func, name='bar', address=address)


    def test_name_field_is_correct_length(self):
        '''
        Test that Warehouse.name must be less than or equal to 64 characters in
        length.

        Note that sqlite does not enforce VARCHAR field length constraints.
        '''
        max_length = 64
        database_engine = settings.DATABASES['default']['ENGINE']
        random_string = (''.join(random.choice(string.ascii_letters +
            string.digits) for _ in range(max_length+1)))
        if database_engine != 'django.db.backends.sqlite3':
            func = Warehouse.objects.create
            self.assertRaises(IntegrityError, func, name=random_string,
                address=Address.objects.create())
