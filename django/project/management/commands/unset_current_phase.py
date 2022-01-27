from django.core.management.base import BaseCommand

from project.models import Project


class Command(BaseCommand):
    help = """
    Removes current phase from all projects
    usage: unset_current_phase
    """

    def handle(self, *args, **options):  # pragma: no cover
        self.stdout.write("Removing current phases")
        for p in Project.objects.all():
            remove_key_data = p.data.pop('current_phase', None)
            remove_key_draft = p.draft.pop('current_phase', None)
            if remove_key_data and not remove_key_draft:
                p.save(update_fields=['data'])
            elif remove_key_draft and not remove_key_data:
                p.save(update_fields=['draft'])
            elif remove_key_data and remove_key_draft:
                p.save(update_fields=['data', 'draft'])
