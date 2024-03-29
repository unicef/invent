# Generated by Django 4.2.3 on 2023-09-04 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi', '0002_countryinclusionlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countryinclusionlog',
            name='data',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='countryinclusionlog',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='solutionlog',
            name='data',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='solutionlog',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
