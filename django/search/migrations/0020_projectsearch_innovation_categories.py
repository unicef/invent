# Generated by Django 2.1 on 2020-09-21 06:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0019_projectsearch_country_office'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsearch',
            name='innovation_categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]
