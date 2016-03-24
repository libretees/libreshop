# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-19 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20160319_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_card_expiration_date',
            field=models.DateField(verbose_name='Expiration Date'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_card_type',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Card Type'),
        ),
    ]