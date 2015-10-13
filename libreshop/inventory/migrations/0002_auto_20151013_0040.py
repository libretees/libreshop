# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='address',
            field=models.ForeignKey(to='shop.Address'),
        ),
        migrations.AddField(
            model_name='location',
            name='inventory',
            field=models.ForeignKey(to='inventory.Inventory'),
        ),
        migrations.AddField(
            model_name='location',
            name='warehouse',
            field=models.ForeignKey(to='inventory.Warehouse'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='alternatives',
            field=models.ManyToManyField(blank=True, related_name='alternatives_rel_+', to='inventory.Inventory'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='attributes',
            field=models.ManyToManyField(through='inventory.Attribute_Value', to='inventory.Attribute'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='warehouses',
            field=models.ManyToManyField(through='inventory.Location', to='inventory.Warehouse'),
        ),
        migrations.AddField(
            model_name='attribute_value',
            name='attribute',
            field=models.ForeignKey(to='inventory.Attribute'),
        ),
        migrations.AddField(
            model_name='attribute_value',
            name='inventory',
            field=models.ForeignKey(to='inventory.Inventory'),
        ),
    ]
