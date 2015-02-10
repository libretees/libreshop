# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('location', models.CharField(blank=True, max_length=1024, null=True)),
                ('state', models.CharField(blank=True, max_length=16, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('saved_product', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('user', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('shipping_address', models.CharField(blank=True, max_length=1024, null=True)),
                ('billing_addresss', models.CharField(blank=True, max_length=1024, null=True)),
                ('payment_card', models.CharField(blank=True, max_length=4, null=True)),
                ('customer', models.ForeignKey(to='shop.Customer')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('sku', models.CharField(blank=True, max_length=8, null=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('slug', models.SlugField(blank=True, max_length=32, null=True)),
                ('teaser', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('attributes', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('saved_product', jsonfield.fields.JSONField(blank=True, null=True)),
                ('gift_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('order', models.ForeignKey(to='shop.Order')),
                ('product', models.ForeignKey(to='shop.Product')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customer',
            name='selected_products',
            field=models.ManyToManyField(through='shop.Cart', to='shop.Product'),
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
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(to='shop.Customer'),
            preserve_default=True,
        ),
    ]
