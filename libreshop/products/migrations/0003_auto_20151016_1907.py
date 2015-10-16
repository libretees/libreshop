# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20151016_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='sub_sku',
            field=models.CharField(null=True, max_length=8),
        ),
    ]
