# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20150205_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='id',
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(null=True, unique=True, max_length=8, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(null=True, max_length=32, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='teaser',
            field=models.CharField(null=True, max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
