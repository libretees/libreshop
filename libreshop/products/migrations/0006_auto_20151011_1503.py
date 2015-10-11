# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute_value',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='attribute_value',
            name='inventory',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='alternatives',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='location',
        ),
        migrations.AlterField(
            model_name='component',
            name='inventory',
            field=models.ForeignKey(blank=True, null=True, to='inventory.Inventory'),
        ),
        migrations.AlterField(
            model_name='component',
            name='quantity',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=8, decimal_places=2),
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='Attribute_Value',
        ),
        migrations.DeleteModel(
            name='Inventory',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
