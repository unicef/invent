# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0087_auto_20201214_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewscore',
            name='status',
            field=models.CharField(choices=[('PD', 'Pending'), ('DR', 'Draft'), ('CMP', 'Complete')], default='PD', max_length=3),
        ),
    ]
