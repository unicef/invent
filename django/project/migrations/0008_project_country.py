# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 21:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0002_auto_20160422_0908'),
        ('project', '0007_auto_20160427_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='country.Country'),
        ),
    ]
