# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-13 13:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0003_country_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='geodata',
        ),
    ]
