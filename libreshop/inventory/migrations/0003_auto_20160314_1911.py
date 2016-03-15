# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-14 19:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_remove_inventory_attributes'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attribute_value',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='attribute_value',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='attribute_value',
            name='inventory',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='Attribute_Value',
        ),
    ]
