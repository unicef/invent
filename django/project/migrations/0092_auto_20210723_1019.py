# Generated by Django 2.1 on 2021-07-23 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0091_auto_20210616_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectportfoliostate',
            name='overall_reviewer_feedback',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='reviewscore',
            name='overall_reviewer_feedback',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
