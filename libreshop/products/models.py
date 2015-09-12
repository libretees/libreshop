from django.db import models
from model_utils.models import TimeStampedModel
from jsonfield import JSONField

# Create your models here.
class Product(TimeStampedModel):
    sku = models.CharField(max_length=8
                          ,null=True
                          ,blank=True)
    name = models.CharField(max_length=32
                           ,null=False
                           ,blank=False
                           ,unique=True)
    featured = models.BooleanField(null=False
                                  ,blank=False
                                  ,default=False)
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
    
    def __str__(self):
        return self.name
