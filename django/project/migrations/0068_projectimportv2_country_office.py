# Generated by Django 2.1 on 2020-03-13 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0048_auto_20200312_1257'),
        ('project', '0067_auto_20190620_0634'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectimportv2',
            name='country_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='country.CountryOffice'),
        ),
    ]
