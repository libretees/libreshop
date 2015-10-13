# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20151013_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='cost',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], decimal_places=2, max_digits=8, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
