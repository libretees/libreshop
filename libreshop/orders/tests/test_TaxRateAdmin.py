from decimal import Decimal
from django.contrib.admin import site
from django.http import HttpRequest
from django.test import TestCase
from ..admin import TaxRateAdmin
from ..models import TaxRate

# Create your tests here.
class TaxRateAdminTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up supplemental test data.
        tax_rate = TaxRate.objects.create(
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

        # Set up basic test.
        self.request = HttpRequest()
        self.admin = TaxRateAdmin(TaxRate, site)
        self.tax_rate = self.admin.get_object(self.request, tax_rate.pk)


    def test_tax_rate_list_display_shows_effective_tax_rate(self):
        '''
        Test that the result given by the OrderAdmin._fulfilled method is the
        same as the result provided by the Order.fulfilled property.
        '''
        result = None
        method = getattr(self.admin, '_tax_rate', None)
        if method:
            result = method(self.tax_rate)

        effective_tax_rate = (
            self.tax_rate.state_tax_rate +
            self.tax_rate.district_tax_rate +
            self.tax_rate.county_tax_rate +
            self.tax_rate.local_tax_rate
        )
        tax_rate = '%s%%' % (effective_tax_rate * 100).normalize()

        self.assertEqual(result, tax_rate)
