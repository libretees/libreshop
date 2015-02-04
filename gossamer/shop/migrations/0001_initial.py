# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('sku', models.CharField(blank=True, unique=True, max_length=8)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('slug', models.SlugField(blank=True, unique=True, max_length=32)),
                ('teaser', models.CharField(blank=True, max_length=128)),
                ('description', models.TextField()),
                ('attributes', jsonfield.fields.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
