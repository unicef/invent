# Generated by Django 2.1 on 2018-08-29 14:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0013_projectsearch_his'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsearch',
            name='donor_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), default=list, size=None),
        ),
        migrations.AddField(
            model_name='projectsearch',
            name='donors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]
