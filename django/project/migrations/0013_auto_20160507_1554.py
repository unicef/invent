# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-07 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_partnerlogo_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerlogo',
            name='data',
            field=models.ImageField(upload_to=''),
        ),
    ]
