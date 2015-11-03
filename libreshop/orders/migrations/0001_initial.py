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
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('shipping_address', models.CharField(null=True, max_length=1024, blank=True)),
                ('billing_addresss', models.CharField(null=True, max_length=1024, blank=True)),
                ('payment_card', models.CharField(null=True, max_length=4, blank=True)),
                ('customer', models.ForeignKey(null=True, to='customers.Customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
