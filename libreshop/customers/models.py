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
    user = models.OneToOneField(User, primary_key=True)
    addresses = models.ManyToManyField('addresses.Address', blank=True)
    selected_products = models.ManyToManyField(
        'products.Variant', through='carts.Cart',
        through_fields=('customer', 'variant')
    )

    def __str__(self):
          return "%s's profile" % self.user


def create_customer(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.create(user=instance)


post_save.connect(create_customer, sender=User)
