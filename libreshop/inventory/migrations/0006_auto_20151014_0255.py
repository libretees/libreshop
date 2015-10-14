# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20151013_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='quantity',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='address',
            field=models.OneToOneField(to='shop.Address'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='name',
            field=models.CharField(unique=True, max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='warehouse',
            unique_together=set([('name', 'address')]),
        ),
    ]
