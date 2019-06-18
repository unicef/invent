from django.core.management.base import BaseCommand

from project.models import Project


class Command(BaseCommand):
    help = "Switch donors in projects from ID to ID"

    def add_arguments(self, parser):
        parser.add_argument('from', type=int)
        parser.add_argument('to', type=int)

    def handle(self, *args, **options):
        donor_from = options['from']
        donor_to = options['to']

        for p in Project.objects.all():
            if p.data and 'donors' in p.data:
                p.data['donors'] = [donor_to if donor == donor_from else donor for donor in p.data.get('donors', [])]
            if p.draft and 'donors' in p.draft:
                p.draft['donors'] = [donor_to if donor == donor_from else donor for donor in p.draft.get('donors', [])]
            p.save()

        self.stdout.write('Replaced all donor ids from {} to {}'.format(donor_from, donor_to))
