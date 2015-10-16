# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20151016_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
