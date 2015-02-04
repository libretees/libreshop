# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='saved_product',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(to='shop.Product'),
            preserve_default=True,
        ),
    ]
