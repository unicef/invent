# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-02 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolkit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolkit',
            name='version',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
