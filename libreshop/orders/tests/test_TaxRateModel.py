import logging
from decimal import Decimal
from django.test import TestCase
from ..models import TaxRate

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class TaxRateModelTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.tax_rate = TaxRate.objects.create(
            state = 'OK',
            state_tax_rate = Decimal(0.043),
            district = 'Test District',
            district_tax_rate = Decimal(0.007),
            county = 'Test County',
            county_tax_rate = Decimal(0.0),
            city = 'Test',
            local_tax_rate = Decimal(0.01),
            postal_code = '12345',
        )


    def test_tax_rate_property_provides_effective_tax_rate(self):
        '''
        Test that the TaxRate.tax_rate property provides the effective tax rate
        within a given jurisdiction.
        '''
        tax_rate = getattr(self.tax_rate, 'tax_rate', None)
        self.assertAlmostEqual(tax_rate, Decimal(0.06), places=4)
