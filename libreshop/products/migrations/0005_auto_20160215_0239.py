# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20160215_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='fulfillment_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
