# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-11 01:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_auto_20171201_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectapproval',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.UserProfile'),
        ),
    ]
