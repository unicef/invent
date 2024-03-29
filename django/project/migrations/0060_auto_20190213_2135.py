# Generated by Django 2.1 on 2019-02-13 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0045_auto_20181106_1410'),
        ('project', '0059_auto_20190212_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectimportv2',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='country.Country'),
        ),
        migrations.AddField(
            model_name='projectimportv2',
            name='donor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='country.Donor'),
        ),
        migrations.AddField(
            model_name='projectimportv2',
            name='draft',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='projectimportv2',
            name='filename',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
