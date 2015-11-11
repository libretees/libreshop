# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customer_selected_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(blank=True, null=True, max_length=64)),
                ('location', models.CharField(blank=True, null=True, max_length=1024)),
                ('state', models.CharField(blank=True, null=True, max_length=16)),
                ('postal_code', models.CharField(blank=True, null=True, max_length=16)),
                ('customer', models.ForeignKey(blank=True, null=True, to='customers.Customer')),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
        ),
    ]
