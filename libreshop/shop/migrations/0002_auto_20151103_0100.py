# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='order',
            field=models.ForeignKey(to='orders.Order'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
