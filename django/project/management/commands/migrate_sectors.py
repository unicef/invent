from django.core.management.base import BaseCommand
from project.models import Project


class Command(BaseCommand):
    help = 'Splits sector into lead_sector and supporting_sector'

    def handle(self, *args, **options):
        for project in Project.objects.all():
            if 'unicef_sector' in project.data:
                project.data['unicef_leading_sector'] = project.data['unicef_sector'][0] if len(
                    project.data['unicef_sector']) > 0 else None
                project.data['supporting_sector'] = project.data['unicef_sector'][1:] if len(
                    project.data['unicef_sector']) > 1 else []
                project.save()
            if 'unicef_sector' in project.draft:
                project.draft['unicef_supporting_sectors'] = project.draft['unicef_sector'][0] if len(
                    project.draft['unicef_sector']) > 0 else None
                project.draft['supporting_sector'] = project.draft['unicef_sector'][1:] if len(
                    project.draft['unicef_sector']) > 1 else []
                project.save()
        self.stdout.write(self.style.SUCCESS(
            'Successfully split sector into lead_sector and supporting_sector'))
