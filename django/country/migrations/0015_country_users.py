# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-27 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20160719_1259'),
        ('country', '0014_country_project_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='User who can update the country', related_name='_country_users_+', to='user.UserProfile'),
        ),
    ]
