# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('location', models.CharField(blank=True, max_length=1024, null=True)),
                ('state', models.CharField(blank=True, max_length=16, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=16, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(to='shop.Customer')),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
    ]
