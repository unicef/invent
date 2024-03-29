# Generated by Django 2.0.7 on 2018-07-16 15:29

from django.db import migrations
from django.contrib.postgres.operations import (
        BtreeGinExtension, CITextExtension,
        TrigramExtension, UnaccentExtension
    )
class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_create_path_user_20170815_1800'),
    ]

    operations = [
        TrigramExtension(),
        BtreeGinExtension(),
        UnaccentExtension(),
        CITextExtension()
    ]
