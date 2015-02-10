# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(null=True, to='shop.Product', blank=True),
            preserve_default=True,
        ),
    ]
