# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20151013_0157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attribute_value',
            options={'verbose_name': 'attribute', 'verbose_name_plural': 'attributes'},
        ),
        migrations.AlterUniqueTogether(
            name='attribute_value',
            unique_together=set([('attribute', 'inventory')]),
        ),
    ]
