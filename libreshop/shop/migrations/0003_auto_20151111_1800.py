# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20151111_1800'),
        ('shop', '0002_auto_20151103_0100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
