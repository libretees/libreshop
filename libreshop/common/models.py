from django.db import models

# Create your models here.
class Inventory(models.Model):

    qux = models.ManyToManyField(
        'Warehouse',
        through='Location',
        through_fields=('inventory', 'warehouse')
    )


class Location(models.Model):

    class Meta:
        unique_together = ('inventory', 'warehouse')

    inventory = models.ForeignKey('Inventory')
    warehouse = models.ForeignKey('Warehouse')
    quantity = models.DecimalField(max_digits=8, decimal_places=2)


class Warehouse(models.Model):

    name = models.CharField(max_length=8, unique=True)
