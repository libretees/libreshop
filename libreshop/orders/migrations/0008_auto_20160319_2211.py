# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-19 22:11
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20160319_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_card_expiration_date',
            field=models.CharField(max_length=8, validators=[django.core.validators.RegexValidator('^(0[1-9]|1[0-2])[/-]\\d{2}$', code='Invalid expiration date', message='Expiration date must be in MM/YY or MM-YY format')], verbose_name='Expiration Date'),
        ),
    ]
