# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20150912_0130'),
        ('shop', '0003_auto_20150908_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(to='products.Product'),
        ),
        migrations.AlterField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(to='products.Product', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(to='products.Product'),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
