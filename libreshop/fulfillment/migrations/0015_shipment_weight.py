# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-27 00:55
from __future__ import unicode_literals

from django.db import migrations
import django_measurement.models


class Migration(migrations.Migration):

    dependencies = [
        ('fulfillment', '0014_auto_20160719_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='weight',
            field=django_measurement.models.MeasurementField(blank=True, measurement_class='Mass', null=True),
        ),
    ]
