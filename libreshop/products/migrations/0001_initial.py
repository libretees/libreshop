# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('sku', models.CharField(null=True, blank=True, max_length=8)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('featured', models.BooleanField(default=False)),
                ('slug', models.SlugField(null=True, blank=True, max_length=32)),
                ('teaser', models.CharField(null=True, blank=True, max_length=128)),
                ('description', models.TextField(null=True, blank=True)),
                ('attributes', jsonfield.fields.JSONField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
