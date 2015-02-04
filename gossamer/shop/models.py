from django.db import models
from django.contrib.auth.models import User

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
    
    def __unicode__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(User)
    product = models.ForeignKey('Product'
                               ,null=False)
    saved_product = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)