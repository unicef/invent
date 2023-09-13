# Generated by Django 2.1 on 2023-08-23 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0109_auto_20230807_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardwareplatform',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hardaware_tags', to='project.Project'),
        ),
        migrations.AddField(
            model_name='nontechplatform',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nontechnology_tags', to='project.Project'),
        ),
        migrations.AddField(
            model_name='platformfunction',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='platform_tags', to='project.Project'),
        ),
        migrations.AddField(
            model_name='technologyplatform',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='software_tags', to='project.Project'),
        ),
    ]