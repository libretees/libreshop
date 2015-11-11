from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.
class Address(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'addresses'

    customer = models.ForeignKey('customers.Customer',
                                 null=True,
                                 blank=True)
    name = models.CharField(max_length=64,
                            null=True,
                            blank=True)
    location = models.CharField(max_length=1024,
                                null=True,
                                blank=True)
    state = models.CharField(max_length=16,
                             null=True,
                             blank=True)
    postal_code = models.CharField(max_length=16,
                                   null=True,
                                   blank=True)
