# Pre-filled data for Scale Phase model

from django.db import migrations


def forwards_func(apps, schema_editor):
    """
    Creates the 6 default values for scale phases which the other models can use
    """
    from project.models import ScalePhase

    for i, dontcare in ScalePhase.SCALE_CHOICES:
        ScalePhase.objects.create(scale=i)


def reverse_func(apps, schema_editor):
    """
    Clears ScalePhase table
    """
    from project.models import ScalePhase

    for i, dontcare in ScalePhase.SCALE_CHOICES:
        ScalePhase.objects.filter(scale=i).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0072_projectportfoliostate_basescore_scalephase_reviewscore'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
