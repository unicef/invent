# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-20 13:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0043_auto_20171220_1021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hscchallenge',
            options={'ordering': ('name',), 'verbose_name': 'Health System Challenge', 'verbose_name_plural': 'Health System Challenges'},
        ),
    ]
