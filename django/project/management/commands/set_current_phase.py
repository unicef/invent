from django.core.management.base import BaseCommand

from project.models import Project, Stage


class Command(BaseCommand):
    help = """
    Sets current phase of all projects calculated from the `stages` field.
    usage: set_current_phase
    """

    def handle(self, *args, **options):  # pragma: no cover
        self.stdout.write("Setting phases")
        for project in Project.objects.all():
            if project.public_id:
                project.data['current_phase'] = Stage.calc_current_phase(project.data.get('stages', []))
            project.draft['current_phase'] = Stage.calc_current_phase(project.draft.get('stages', []))
            project.save(update_fields=['draft', 'data'])
