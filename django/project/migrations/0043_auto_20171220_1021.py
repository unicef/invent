# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-20 10:21
from __future__ import unicode_literals

from django.db import migrations
from django.db.models.expressions import F


def fix_hidden_translated_values(apps, schema_editor):
    HSCGroup = apps.get_model('project', 'HSCGroup')
    HSCChallenge = apps.get_model('project', 'HSCChallenge')

    HSCGroup.all_objects.update(name_en=F('name'))
    HSCChallenge.objects.update(name_en=F('name'))


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0042_auto_20171220_0947'),
    ]

    operations = [
        migrations.RunPython(fix_hidden_translated_values, migrations.RunPython.noop),
    ]
