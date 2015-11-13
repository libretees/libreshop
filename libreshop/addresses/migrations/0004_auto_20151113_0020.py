# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_auto_20151113_0016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='post_code',
            new_name='postal_code',
        ),
    ]
