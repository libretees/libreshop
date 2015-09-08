# Import Python module(s)
import logging

# Import Django module(s)
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

# Import 3rd-Party module(s)
from model_utils.models import TimeStampedModel


# Initialize logger
logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


# Create your models here.
class Customer(TimeStampedModel):
    user = models.OneToOneField(User,
                                primary_key=True)
    selected_products = models.ManyToManyField('shop.Product',
                                               through='shop.Cart',
                                               through_fields=('customer', 'product'))

    def __str__(self):
          return "%s's profile" % self.user


def create_customer(sender, **kw):
    user = kw['instance']
    if kw['created']:
        customer = Customer(user=user)
        customer.save()


post_save.connect(create_customer, sender=User)
