from django.core.management.base import BaseCommand

from project.models import Project


class Command(BaseCommand):
    help = """
    Rebuild search DB
    usage: rebuild_search
    """

    def handle(self, *args, **options):  # pragma: no cover
        self.stdout.write("Rebuilding search")
        for project in Project.objects.exclude(public_id=""):
            project.search.update(project)
