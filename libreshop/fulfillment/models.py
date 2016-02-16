import logging
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Manufacturer(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    fulfillment_backend = models.CharField(
        max_length=128, null=False, blank=False
    )
    fulfillment_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class DropShipmentSetting(TimeStampedModel):

    class Meta:
        unique_together = ('manufacturer', 'name')

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)

    def __str__(self):
        return '%s: %s' % (self.manufacturer.name, self.name)


class DropShipmentSettingValue(TimeStampedModel):

    class Meta:
        verbose_name = 'Drop Shipment Setting'
        verbose_name_plural = 'Drop Shipment Settings'
        unique_together = ('setting', 'variant')

    setting = models.ForeignKey(
        'DropShipmentSetting', null=True, blank=True
    )
    variant = models.ForeignKey('products.Variant', null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)
