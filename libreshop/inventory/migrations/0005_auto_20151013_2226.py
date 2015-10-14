# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20151013_2214'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attribute_value',
            unique_together=set([('inventory', 'attribute')]),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('inventory', 'warehouse')]),
        ),
    ]
