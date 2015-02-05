# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20150205_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='saved_product',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
