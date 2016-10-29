import logging
from django.core.exceptions import MultipleObjectsReturned
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

        # Strip whitespace from the beginning & end of fields prior to lookup
        # or save.
        field_names = ('recipient_name', 'street_address', 'locality', 'region',
            'postal_code')
        for field_name in field_names:
            value = getattr(self, field_name)
            stripped_value = value.strip() if value else None
            setattr(self, field_name, stripped_value)

        logger.debug('Retrieving Address...')
        address = None
        try:
            address = Address.objects.get(**{
                field_name:getattr(self, field_name)
                for field_name in field_names})
        except Address.DoesNotExist as e:
            logger.debug('No address found!')
        except MultipleObjectsReturned as e:
            logger.debug('Multiple records found!')
            address = Address.objects.filter(**{
                field_name:getattr(self, field_name)
                for field_name in field_names}).last()
        else:
            logger.debug('Address found (%s)!' % str(address))
        finally:
            self.pk = getattr(address, 'pk', None)

        if address is None:
            logger.debug('Creating Address...')
            super(Address, self).save(*args, **kwargs)
            logger.debug('Created Address (%s).' % str(self))
