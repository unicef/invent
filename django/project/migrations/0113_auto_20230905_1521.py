# Generated by Django 2.1 on 2023-09-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0112_reorder_stages'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='set_aside_2021',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='solution',
            name='set_aside_2022',
            field=models.BooleanField(default=False),
        ),
    ]