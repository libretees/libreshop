# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(null=True, max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attribute_Value',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('value', models.CharField(null=True, max_length=64, blank=True)),
                ('attribute', models.ForeignKey(to='inventory.Attribute')),
            ],
            options={
                'verbose_name_plural': 'attribute values',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(null=True, max_length=64, blank=True)),
                ('quantity', models.DecimalField(max_digits=8, decimal_places=2)),
                ('cost', models.DecimalField(max_digits=8, decimal_places=2)),
                ('alternatives', models.ManyToManyField(related_name='alternatives_rel_+', to='inventory.Inventory')),
                ('attributes', models.ManyToManyField(to='inventory.Attribute', through='inventory.Attribute_Value')),
            ],
            options={
                'verbose_name_plural': 'inventory',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('name', models.CharField(null=True, max_length=64, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='inventory',
            name='location',
            field=models.ForeignKey(to='inventory.Location'),
        ),
        migrations.AddField(
            model_name='attribute_value',
            name='inventory',
            field=models.ForeignKey(to='inventory.Inventory'),
        ),
    ]
