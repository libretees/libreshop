# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20151004_0310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute_Value',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('value', models.CharField(max_length=64, blank=True, null=True)),
                ('attribute', models.ForeignKey(to='products.Attribute')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='attribute_values',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='attribute_values',
            name='inventory',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='attributes',
            field=models.ManyToManyField(to='products.Attribute', through='products.Attribute_Value'),
        ),
        migrations.DeleteModel(
            name='Attribute_Values',
        ),
        migrations.AddField(
            model_name='attribute_value',
            name='inventory',
            field=models.ForeignKey(to='products.Inventory'),
        ),
    ]
