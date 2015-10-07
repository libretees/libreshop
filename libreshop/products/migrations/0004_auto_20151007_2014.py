# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20151005_0045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attribute_value',
            options={'verbose_name_plural': 'attribute values'},
        ),
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name_plural': 'inventory'},
        ),
        migrations.AlterField(
            model_name='component',
            name='inventory',
            field=models.ForeignKey(blank=True, to='products.Inventory', null=True),
        ),
        migrations.AlterField(
            model_name='component',
            name='quantity',
            field=models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('1')),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(unique=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='variant',
            name='price',
            field=models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00')),
        ),
    ]
