# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='postal_code',
            new_name='post_code',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='location',
            new_name='street',
        ),
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
        migrations.AddField(
            model_name='address',
            name='locality',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
