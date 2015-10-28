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
            field=models.OneToOneField(to='shop.Address'),
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
            field=models.ManyToManyField(related_name='alternatives_rel_+', to='inventory.Inventory', blank=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='attributes',
            field=models.ManyToManyField(to='inventory.Attribute', through='inventory.Attribute_Value'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='warehouses',
            field=models.ManyToManyField(to='inventory.Warehouse', through='inventory.Location'),
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
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('inventory', 'warehouse')]),
        ),
        migrations.AlterUniqueTogether(
            name='attribute_value',
            unique_together=set([('inventory', 'attribute')]),
        ),
    ]
