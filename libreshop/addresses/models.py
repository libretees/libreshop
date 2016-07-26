import logging
from django.db import models
from django.utils.safestring import mark_safe
from model_utils.models import TimeStampedModel
from django_countries.fields import CountryField

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Address(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'addresses'

    # Name of the recipient at this address.
    recipient_name = models.CharField(max_length=64, null=True, blank=True)
    # Field for street address.
    street_address = models.CharField(max_length=1024, null=False, blank=False)
    # Field for City/Town.
    locality = models.CharField(max_length=16, null=False, blank=False)
    # Field for State/Province/County.
    region = models.CharField(max_length=16, null=True, blank=True)
    # Field for ZIP/Postal Code.
    postal_code = models.CharField(max_length=16, null=True, blank=True)
    # Field for Country.
    country = CountryField(null=False, blank=False)

    def __str__(self):

        postal_region = (
            '%s %s' % (self.region, self.postal_code)
            if (self.region and self.postal_code) else self.postal_code)

        address_fields = [
            self.recipient_name, self.street_address.replace('\r\n', ', '),
            self.locality, postal_region, str(self.country.name)]

        populated_address_fields = [
            field for field in address_fields if field]

        return ', '.join(populated_address_fields)

    def render(self):
        address = '<br />'.join([
            self.recipient_name, self.street_address.replace('\r\n', '<br />'),
            ('%s, %s  %s' % (self.locality, self.region, self.postal_code)),
            str(self.country.name)
        ])

        return mark_safe(address)

    def save(self, *args, **kwargs):

        logger.debug('Retrieving Address...')
        address = None
        try:
            address = Address.objects.get(
                recipient_name = self.recipient_name.strip(),
                street_address = self.street_address.strip(),
                locality = self.locality.strip(),
                region = self.region.strip(),
                postal_code = self.postal_code.strip(),
                country = self.country
            )
        except Address.DoesNotExist as e:
            logger.debug('No address found!')
        else:
            logger.debug('Address found (%s)!' % str(address))
            self.pk = address.pk

        if address is None:
            logger.debug('Creating Address...')

            # Strip whitespace from the beginning & end of fields prior to save.
            for field in ['recipient_name', 'street_address', 'locality',
                'region', 'postal_code']:
                setattr(self, field, getattr(self, field).strip())

            address = super(Address, self).save(*args, **kwargs)
            logger.debug('Created Address (%s).' % str(self))

        return address
