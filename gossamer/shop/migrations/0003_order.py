# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('shipping_address', models.CharField(null=True, blank=True, max_length=1024)),
                ('billing_addresss', models.CharField(null=True, blank=True, max_length=1024)),
                ('payment_card', models.CharField(null=True, blank=True, max_length=4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(to='shop.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
