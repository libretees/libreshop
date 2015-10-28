from django.db import models
from jsonfield import JSONField
from model_utils.models import TimeStampedModel

# Create your models here.
class Cart(TimeStampedModel):
    customer = models.ForeignKey('customers.Customer', null=False)
    product = models.ForeignKey('products.Product', null=False)
    saved_product = JSONField(null=True, blank=True)
