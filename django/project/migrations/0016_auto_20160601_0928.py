# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_team_users(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Project = apps.get_model("project", "Project")
    UserProfile = apps.get_model("user", "UserProfile")

    for user in UserProfile.objects.all():
        project = Project.projects.by_organisation(user.organisation).first()
        if project:
            project.team.add(user)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('user', '0002_auto_20160428_0952'),
        ('project', '0015_auto_20160601_0928'),
    ]

    operations = [
        migrations.RunPython(add_team_users),
    ]