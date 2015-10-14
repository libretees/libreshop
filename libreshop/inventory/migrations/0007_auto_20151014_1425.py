# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20151014_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute_value',
            name='value',
            field=models.CharField(max_length=64),
        ),
    ]
