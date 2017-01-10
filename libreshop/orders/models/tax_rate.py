import logging
from decimal import Decimal
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

class TaxRate(TimeStampedModel):

    state = models.CharField(max_length=64, null=True, blank=True)
    district = models.CharField(max_length=64, null=True, blank=True)
    county = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    postal_code = models.CharField(max_length=16, null=True, blank=True)

    state_tax_rate = models.DecimalField(max_digits=5, decimal_places=4,
        null=False, blank=False, default=Decimal('0.00'))
    district_tax_rate = models.DecimalField(max_digits=5, decimal_places=4,
        null=False, blank=False, default=Decimal('0.00'))
    county_tax_rate = models.DecimalField(max_digits=5, decimal_places=4,
        null=False, blank=False, default=Decimal('0.00'))
    local_tax_rate = models.DecimalField(max_digits=5, decimal_places=4,
        null=False, blank=False, default=Decimal('0.00'))

    @property
    def tax_rate(self):
        return (
            self.local_tax_rate + self.county_tax_rate +
            self.district_tax_rate + self.state_tax_rate
        )

    def __str__(self):
        return '%s, %s %s' % (self.city, self.state, self.postal_code)

    class Meta:
        verbose_name = 'Tax Rate'
        unique_together = ('state', 'district', 'county', 'city', 'postal_code')
