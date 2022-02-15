# Generated by Django 2.1 on 2022-02-14 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_auto_20220121_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('fr', 'French'), ('es', 'Spanish'), ('pt', 'Portuguese')], default='en', max_length=2),
        ),
    ]
