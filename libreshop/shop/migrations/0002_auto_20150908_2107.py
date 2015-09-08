# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='selected_products',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AlterField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(to='customers.Customer'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(to='customers.Customer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(to='customers.Customer'),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
