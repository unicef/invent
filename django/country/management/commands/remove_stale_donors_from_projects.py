from django.core.management.base import BaseCommand

from project.models import Project


class Command(BaseCommand):
    help = "Remove stale donors from projects and rebuild search"

    def handle(self, *args, **options):
        stale_ids = Project.remove_stale_donors()
        self.stdout.write('Removed {} donors'.format(len(set(stale_ids))))
