from django.conf import settings
from django.db import models

from jsonfield import JSONField

class Product(models.Model):
    sku = models.CharField(max_length=8
                          ,blank=True
                          ,unique=True)
    name = models.CharField(max_length=32
                           ,blank=False
                           ,unique=True)
    slug = models.SlugField(max_length=32
                           ,blank=True
                           ,unique=True
                           ,db_index=True)
    teaser = models.CharField(max_length=128
                             ,blank=True) 
    description = models.TextField()
    attributes = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey('Customer'
                                ,null=False)
    product = models.ForeignKey('Product'
                               ,null=False)
    saved_product = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    #other fields here
    selected_products = models.ManyToManyField(Product, through='Cart', through_fields=('customer', 'product'))

    def __str__(self):
          return "%s's profile" % self.user

