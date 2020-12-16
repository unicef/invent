from django.core.management.base import BaseCommand
from django.db.models import Q

from project.models import Project
from project.utils import migrate_project_phases


class Command(BaseCommand):
    help = """
    Migrate project with old phases
    """

    def handle(self, *args, **options):
        projects = Project.objects.filter(Q(data__has_key='phase') | Q(draft__has_key='phase'))
        conflicting_projects = Project.objects.filter(data__has_key='stages') \
            .filter(Q(data__has_key='phase') | Q(draft__has_key='phase'))
        self.stdout.write(f'Migrating {projects.count()} initiatives')
        self.stdout.write(f'DEBUG IDs {list(projects.values_list("id", flat=True))}')
        self.stdout.write(f'DEBUG NAMEs {list(projects.values_list("name", flat=True))}')

        if conflicting_projects:
            self.stdout.write('')
            self.stdout.write(f'WARNING: {conflicting_projects.count()} initiatives have both stages and phase set')
            self.stdout.write(f'DEBUG IDs {list(conflicting_projects.values_list("id", flat=True))}')
            self.stdout.write(f'DEBUG NAMEs {list(conflicting_projects.values_list("name", flat=True))}')

            confirm = input('Do you still want to migrate? (y/n)')
            if confirm != 'y':
                return

        for p in projects:
            migrate_project_phases(p)
