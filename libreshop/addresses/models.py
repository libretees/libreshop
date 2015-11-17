from django.db import models
from model_utils.models import TimeStampedModel
from django_countries.fields import CountryField

# Create your models here.
class Address(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'addresses'

    customer = models.ForeignKey('customers.Customer', null=True, blank=True)
    # Name of the recipient at this address.
    recipient_name = models.CharField(max_length=64, null=True, blank=True)
    # Field for street address.
    street_address = models.CharField(max_length=1024, null=False, blank=False)
    # Field for City/Town.
    municipality = models.CharField(max_length=16, null=False, blank=False)
    # Field for State/Province/Region.
    region = models.CharField(max_length=16, null=False, blank=False)
    # Field for ZIP/Postal Code.
    postal_code = models.CharField(max_length=16, null=True, blank=True)
    # Field for country.
    country = CountryField(null=False, blank=False)
