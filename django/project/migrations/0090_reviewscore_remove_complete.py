# Generated manually

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('project', '0089_reviewscore_fill_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewscore',
            name='complete',
        ),
    ]