import importlib
import logging
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Supplier(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    fulfillment_backend = models.CharField(
        max_length=128, null=False, blank=False
    )
    fulfillment_time = models.TimeField(null=True, blank=True)


    def load_fulfillment_backend(self):

        backend = self.fulfillment_backend
        index = backend.rfind('.')
        module_name, attribute_name = backend[:index], backend[index+1:]
        module, attribute = None, None
        try:
            module = importlib.import_module(module_name)
            attribute = getattr(module, attribute_name)
        except ImportError as e:
            logger.critical('Unable to import module \'%s\'.' % module_name)
        except AttributeError as e:
            logger.critical('\'%s\' module has no attribute \'%s\'.' %
                (module_name, attribute_name))

        return attribute


    def __str__(self):
        return self.name


class FulfillmentSetting(TimeStampedModel):

    class Meta:
        unique_together = ('supplier', 'name')

    supplier = models.ForeignKey('Supplier', null=True, blank=True)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)

    def __str__(self):
        return '%s: %s' % (self.supplier.name, self.name)


class FulfillmentSettingValue(TimeStampedModel):

    class Meta:
        verbose_name = 'Fulfillment Setting'
        verbose_name_plural = 'Fulfillment Settings'
        unique_together = ('setting', 'variant')

    setting = models.ForeignKey(
        'FulfillmentSetting', null=True, blank=True
    )
    variant = models.ForeignKey('products.Variant', null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)
