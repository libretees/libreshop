from django.test import TestCase
from ..models import FulfillmentSetting, Supplier

# Create your tests here.
class FulfillmentSettingModelTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.supplier = Supplier.objects.create(
            name='foo',
            fulfillment_backend='django.core.mail.backends.locmem.EmailBackend'
        )
        self.setting = FulfillmentSetting.objects.create(
            supplier=self.supplier, name='bar'
        )


    def test_model_string_representation(self):
        '''
        Test that the FulfillmentSetting string representation displays
        properly.
        '''
        self.assertEqual(str(self.setting), 'foo: bar')
