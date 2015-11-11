# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20151028_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='address',
            field=models.OneToOneField(to='addresses.Address'),
        ),
    ]
