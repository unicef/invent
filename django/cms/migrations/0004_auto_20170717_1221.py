# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-17 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20170516_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=140, unique=True),
        ),
    ]
