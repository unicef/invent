# Generated by Django 2.1 on 2019-01-21 14:44

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('search', '0014_auto_20180829_1456'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectsearch',
            old_name='hsc_categories',
            new_name='hsc',
        )
    ]
