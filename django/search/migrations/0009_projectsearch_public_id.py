# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-21 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_auto_20170517_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsearch',
            name='public_id',
            field=models.TextField(blank=True),
        ),
    ]
