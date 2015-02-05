# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('saved_product', jsonfield.fields.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('sku', models.CharField(max_length=8, unique=True, blank=True)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('slug', models.SlugField(max_length=32, unique=True, blank=True)),
                ('teaser', models.CharField(max_length=128, blank=True)),
                ('description', models.TextField()),
                ('attributes', jsonfield.fields.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customer',
            name='selected_products',
            field=models.ManyToManyField(to='shop.Product', through='shop.Cart'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(to='shop.Customer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(to='shop.Product'),
            preserve_default=True,
        ),
    ]
