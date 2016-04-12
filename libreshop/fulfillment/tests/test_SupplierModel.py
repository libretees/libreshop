from django.test import TestCase
from ..models import FulfillmentSetting, Supplier

# Create your tests here.
class SupplierModelTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.supplier = Supplier.objects.create(
            name='foo',
            fulfillment_backend='django.core.mail.backends.locmem.EmailBackend'
        )


    def test_model_will_not_load_invalid_module(self):
        '''
        Test that the model gracefully handles an attempt to load an invalid
        module.
        '''
        self.supplier.fulfillment_backend = 'foo'
        self.supplier.save()

        fulfillment_backend = self.supplier.load_fulfillment_backend()

        self.assertIsNone(fulfillment_backend)


    def test_model_will_not_load_invalid_attribute(self):
        '''
        Test that the model gracefully handles an attempt to load an invalid
        module attribute.
        '''
        self.supplier.fulfillment_backend = 'django.core.mail.backends.foo'
        self.supplier.save()

        fulfillment_backend = self.supplier.load_fulfillment_backend()

        self.assertIsNone(fulfillment_backend)


    def test_model_can_load_valid_fulfillment_backend(self):
        '''
        Test that the model can load a valid module.
        '''
        fulfillment_backend = self.supplier.load_fulfillment_backend()
        self.assertIsNotNone(fulfillment_backend)


    def test_model_string_representation(self):
        '''
        Test that the Supplier string representation displays properly.
        '''
        self.assertEqual(str(self.supplier), 'foo')
