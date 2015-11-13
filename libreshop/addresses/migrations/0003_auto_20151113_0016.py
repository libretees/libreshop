# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20151113_0006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='name',
            new_name='recipient_name',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='street',
            new_name='street_address',
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='region',
            field=models.CharField(null=True, max_length=16, blank=True),
        ),
    ]
