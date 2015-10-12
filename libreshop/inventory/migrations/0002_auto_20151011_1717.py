# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=64, blank=True, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='inventory',
            name='location',
            field=models.ForeignKey(to='inventory.InventoryLocation'),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
