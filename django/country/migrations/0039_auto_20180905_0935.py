# Generated by Django 2.1 on 2018-09-05 09:35
from django.db import migrations
import uuid


def fill_code(apps, schema_editor):
    Donor = apps.get_model('country', 'Donor')
    for donor in Donor.objects.all():
        donor.code = uuid.uuid4().hex[:10]
        donor.save()


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0038_auto_20180905_0935'),
    ]

    operations = [
        migrations.RunPython(fill_code, reverse_code=migrations.RunPython.noop)
    ]
