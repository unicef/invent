from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import make_aware
from datetime import datetime

from project.models import Project, ProjectVersion


class Command(BaseCommand):
    help = 'Restore modified date of projects to the last modified date before 2023-07-06'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING(
            'Rollback Project modified dates from ProjectVersion...'))
        # Get the date '2023-07-6' as a timezone-aware datetime object
        cutoff_date = make_aware(datetime(2023, 7, 6))

        # Fetch all projects that were modified on '2023-07-06'
        projects = Project.objects.filter(modified__date=cutoff_date)

        # Start a new transaction
        with transaction.atomic():
            # For each project, find the last change before '2023-07-06' and use that as the new 'modified' value
            for project in projects:
                last_version = ProjectVersion.objects.filter(
                    project_id=project.id,
                    modified__lt=cutoff_date
                ).order_by('modified').last()
                if last_version is not None:
                    # Use Django's update() method to bypass the automatic update of the 'modified' field
                    Project.objects.filter(id=project.id).update(
                        modified=last_version.modified)

        self.stdout.write(self.style.SUCCESS(
            'Successfully restored modified dates.'))
