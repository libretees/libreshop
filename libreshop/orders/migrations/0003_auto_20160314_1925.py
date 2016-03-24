# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-14 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='credit_card_last_4',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Last 4'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(max_length=8, unique=True, verbose_name='ID'),
        ),
    ]