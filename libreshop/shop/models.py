import logging
from django.db import models
from model_utils.models import TimeStampedModel
from jsonfield import JSONField
from customers.models import Customer
from products.models import Product

logger = logging.getLogger(__name__)


class Cart(TimeStampedModel):
    customer = models.ForeignKey(Customer,
                                 null=False)
    product = models.ForeignKey(Product,
                                null=False)
    saved_product = JSONField(null=True,
                              blank=True)


class Address(TimeStampedModel):
    
    class Meta():
        verbose_name_plural = 'addresses'

    customer = models.ForeignKey(Customer,
                                 null=False)   
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



class Order(TimeStampedModel):
    customer = models.ForeignKey(Customer,
                                 null=False)
    shipping_address = models.CharField(max_length=1024,
                                        null=True,
                                        blank=True)
    billing_addresss = models.CharField(max_length=1024,
                                        null=True,
                                        blank=True) 
    payment_card = models.CharField(max_length=4,
                                    null=True,
                                    blank=True)


class Purchase(TimeStampedModel):
    order = models.ForeignKey(Order,
                              null=False)
    product = models.ForeignKey(Product,
                                null=False)
    saved_product = JSONField(null=True,
                              blank=True)
    gift_amount = models.DecimalField(max_digits=8,
                                      decimal_places=2)


class Category(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'categories'

    parent_category = models.ForeignKey('self',
                                        null=True,
                                        blank=True)
    name = models.CharField(max_length=32,
                            null=False,
                            blank=False,
                            unique=True)
    slug = models.SlugField(max_length=32,
                            null=True,
                            blank=True,
                            db_index=True)
    products = models.ManyToManyField(Product,
                                      blank=True)

    def __str__(self):
          return self.name
