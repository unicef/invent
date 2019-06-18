from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from project.models import Project, HISBucket, HSCChallenge, InteroperabilityLink, InteroperabilityStandard, Licence, \
    TechnologyPlatform


class Command(BaseCommand):
    help = 'Converts string values to IDs in the project.data JSON'

    def add_arguments(self, parser):
        parser.add_argument('project_id', nargs='*', type=int)

    def handle(self, *args, **options):
        self.stdout.write("-- Moving string values to IDs --")

        his_bucket_mapping = {hb.name: hb.id for hb in HISBucket.all_objects.all()}

        hsc_challenge_mapping = {hsc.challenge: hsc.id for hsc in HSCChallenge.all_objects.all()}

        interoperability_link_mapping = {i.name: i.id for i in InteroperabilityLink.all_objects.all()}

        # Create missing value
        InteroperabilityStandard.all_objects.create(name='JSON')
        interoperability_standard_mapping = {i.name: i.id for i in InteroperabilityStandard.all_objects.all()}

        # Create missing value
        Licence.all_objects.create(name='WHO server')
        license_mapping = {l.name: l.id for l in Licence.all_objects.all()}

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

            project.data['his_bucket'] = [bn if isinstance(bn, int) else his_bucket_mapping[bn]
                                          for bn in project.data['his_bucket']]

            project.data['hsc_challenges'] = [hsc if isinstance(hsc, int) else hsc_challenge_mapping[hsc]
                                              for hsc in project.data['hsc_challenges']]

            for link in project.data['interoperability_links']:
                if 'id' in link:
                    continue

                name = link.pop('name')
                link['id'] = interoperability_link_mapping[name]

            project.data['interoperability_standards'] = [i if isinstance(i, int)
                                                          else interoperability_standard_mapping[i]
                                                          for i in project.data['interoperability_standards']]

            project.data['licenses'] = [l if isinstance(l, int) else license_mapping[l]
                                        for l in project.data['licenses']]

            project.data['platforms'] = [p if 'id' in p else {'id': platform_mapping[p['name']], 'strategies': []}
                                         for p in project.data['platforms']]

            project.data['health_focus_areas'] = []
            project.data['name'] = project.name

            project.draft = project.data

            project.save()

            self.stdout.write('- Finished on project {} -'.format(project.id))
