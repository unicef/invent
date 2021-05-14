# Generated manually

from django.db import migrations

def migrate_completion_data(apps, schema_editor):
    ReviewScore = apps.get_model('project', 'ReviewScore')
    for score in ReviewScore.objects.filter(complete=True):
        score.status = 'CMP'
        score.save()


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0088_reviewscore_add_status'),
    ]

    operations = [
        migrations.RunPython(migrate_completion_data, migrations.RunPython.noop),
    ]
