# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_auto_20151113_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='locality',
            field=models.CharField(max_length=16, default='Foo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='region',
            field=models.CharField(max_length=16, default='Bar'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='street_address',
            field=models.CharField(max_length=1024, default='Baz'),
            preserve_default=False,
        ),
    ]
