from django.core.management.base import BaseCommand
from project.models import Phase


class Command(BaseCommand):
    help = """
    Fill phases mapping table (the old, deprecated one)
    """

    def handle(self, *args, **options):  # pragma: no cover
        phases = {
            '01. Opportunity and Ideation',
            '02. Preparation and Scoping',
            '03. Analysis and Design',
            '04. Implementation Planning',
            '05. Developing or Adapting Solution',
            '06. Piloting and Evidence Generation',
            '07. Package and Advocacy',
            '08. Deploying',
            '09. Scaling Up',
            '10. Handover or Complete',
            '11. Discontinued',
            '12. External',
            '13. Under Review',
            'N/A'
        }
        for phase in phases:
            _, created = Phase.objects.get_or_create(name=phase)
            if created:
                self.stdout.write(f'Created phase: {phase}')

        self.stdout.write("Phase mapping success")
