# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20151016_1907'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='variant',
            unique_together=set([('product', 'sub_sku'), ('product', 'name')]),
        ),
    ]
