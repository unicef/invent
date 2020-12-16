from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from project.models import Project, HSCChallenge, TechnologyPlatform


class Command(BaseCommand):
    help = 'Converts string values to IDs in the project.data JSON'

    def add_arguments(self, parser):
        parser.add_argument('project_id', nargs='*', type=int)

    def handle(self, *args, **options):
        self.stdout.write("-- Moving string values to IDs --")

        hsc_challenge_mapping = {hsc.challenge: hsc.id for hsc in HSCChallenge.all_objects.all()}

        # Create missing values
        TechnologyPlatform.all_objects.create(name='Vumi')
        TechnologyPlatform.all_objects.create(name='Custom Built from eHA')
        TechnologyPlatform.all_objects.create(name='Hoji')
        platform_mapping = {p.name: p.id for p in TechnologyPlatform.all_objects.all()}

        project_qs = Project.projects.all()

        if options['project_id']:
            project_qs = project_qs.filter(id__in=options['project_id'])

        for project in project_qs:
            self.stdout.write('- Working on project {} -'.format(project.id))

            project.data['hsc_challenges'] = [hsc if isinstance(hsc, int) else hsc_challenge_mapping[hsc]
                                              for hsc in project.data['hsc_challenges']]

            project.data['platforms'] = [p if 'id' in p else {'id': platform_mapping[p['name']], 'strategies': []}
                                         for p in project.data['platforms']]

            project.data['health_focus_areas'] = []
            project.data['name'] = project.name

            project.draft = project.data

            project.save()

            self.stdout.write('- Finished on project {} -'.format(project.id))
