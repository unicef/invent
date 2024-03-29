# Generated by Django 2.1 on 2019-06-19 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0065_auto_20190619_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='digitalstrategy',
            options={'ordering': ['group', 'name'], 'verbose_name': 'WHO Digital Health Intervention (DHI)', 'verbose_name_plural': 'WHO Digital Health Interventions (DHIs)'},
        ),
        migrations.AlterModelOptions(
            name='healthcategory',
            options={'ordering': ['name'], 'verbose_name': 'WHO Health Category', 'verbose_name_plural': 'WHO Health Categories'},
        ),
        migrations.AlterModelOptions(
            name='healthfocusarea',
            options={'ordering': ['health_category__name', 'name'], 'verbose_name': 'WHO Health Focus Area', 'verbose_name_plural': 'WHO Health Focus Areas'},
        ),
        migrations.AlterModelOptions(
            name='hscchallenge',
            options={'ordering': ['group', 'name'], 'verbose_name': 'WHO Health System Challenge', 'verbose_name_plural': 'WHO Health System Challenges'},
        ),
        migrations.AlterModelOptions(
            name='hscgroup',
            options={'ordering': ['name'], 'verbose_name': 'WHO Health System Challenge Group'},
        ),
        migrations.AlterModelOptions(
            name='technologyplatform',
            options={'ordering': ['name'], 'verbose_name': 'Platform', 'verbose_name_plural': 'Platforms'},
        ),
    ]
