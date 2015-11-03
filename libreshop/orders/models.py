from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.
class Order(TimeStampedModel):
    customer = models.ForeignKey('customers.Customer', null=True, blank=True)
    shipping_address = models.CharField(max_length=1024, null=True, blank=True)
    billing_addresss = models.CharField(max_length=1024, null=True, blank=True)
    payment_card = models.CharField(max_length=4, null=True, blank=True)
