# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-18 17:20
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fulfillment', '0008_auto_20160529_0110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('carrier', models.CharField(max_length=32, unique=True, verbose_name='ID')),
                ('tracking_number', models.CharField(max_length=64, unique=True, verbose_name='ID')),
                ('shipping_cost', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fulfillment.FulfillmentOrder')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]