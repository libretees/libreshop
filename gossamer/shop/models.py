from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from jsonfield import JSONField

User = settings.AUTH_USER_MODEL

class Product(models.Model):
    sku = models.CharField(max_length=8
                          ,null=True
                          ,blank=True)
    name = models.CharField(max_length=32
                           ,null=False
                           ,blank=False
                           ,unique=True)
    slug = models.SlugField(max_length=32
                           ,null=True
                           ,blank=True
                           ,db_index=True)
    teaser = models.CharField(max_length=128
                             ,null=True
                             ,blank=True) 
    description = models.TextField(null=True
                                  ,blank=True)
    attributes = JSONField(null=True
                          ,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey('Customer'
                                ,null=False)
    product = models.ForeignKey('Product'
                               ,null=False)
    saved_product = JSONField(null=True
                             ,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    id = models.OneToOneField(User
                             ,primary_key=True)
    selected_products = models.ManyToManyField(Product, through='Cart', through_fields=('customer', 'product'))

    def __str__(self):
          return "%s's profile" % self.id


def create_customer(sender, **kw):
    user = kw['instance']
    if kw['created']:
        customer = Customer(id=user)
        customer.save()


post_save.connect(create_customer, sender=User)


class Address(models.Model):
    customer = models.ForeignKey('Customer'
                                ,null=False)   
    name = models.CharField(max_length=64
                           ,null=True
                           ,blank=True)
    location = models.CharField(max_length=1024
                               ,null=True
                               ,blank=True)
    state = models.CharField(max_length=16
                            ,null=True
                            ,blank=True)
    postal_code = models.CharField(max_length=16
                                  ,null=True
                                  ,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta():
        verbose_name_plural = 'addresses'
        
        
class Order(models.Model):
    customer = models.ForeignKey('Customer'
                                ,null=False)
    shipping_address = models.CharField(max_length=1024
                                       ,null=True
                                       ,blank=True)
    billing_addresss = models.CharField(max_length=1024
                                       ,null=True
                                       ,blank=True) 
    payment_card = models.CharField(max_length=4
                                   ,null=True
                                   ,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

