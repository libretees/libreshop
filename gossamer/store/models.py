from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return self.name
    
# Create your models here.
