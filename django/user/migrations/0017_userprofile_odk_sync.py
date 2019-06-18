# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-03 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_auto_20180103_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='odk_sync',
            field=models.BooleanField(default=False, verbose_name='Whether user has been synced with ODK'),
        ),
    ]
