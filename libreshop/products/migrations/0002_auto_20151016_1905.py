# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='inventory',
            field=models.ForeignKey(to='inventory.Inventory', null=True),
        ),
    ]
