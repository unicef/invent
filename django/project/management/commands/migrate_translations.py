import json

from django.core.management.base import BaseCommand
from country.models import Country
from project.models import DigitalStrategy, InteroperabilityLink, HealthCategory, HealthFocusArea, HISBucket, \
    HSCChallenge, HSCGroup, InteroperabilityStandard, TechnologyPlatform, Licence

FILES_CLASSES_FIELDS = [
    ('Country.json', Country, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('DigitalStrategy.json', DigitalStrategy, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('HealthCategory.json', HealthCategory, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('HealthFocusArea.json', HealthFocusArea, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('HISBucket.json', HISBucket, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('HSCChallenge.json', HSCChallenge, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('HSCGroup.json', HSCGroup, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('InteroperabilityLink.json', InteroperabilityLink,
     ['pre_fr', 'pre_es', 'pre_pt', 'pre_ar', 'name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('InteroperabilityStandard.json', InteroperabilityStandard, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('Licence.json', Licence, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
    ('TechnologyPlatform.json', TechnologyPlatform, ['name_fr', 'name_es', 'name_pt', 'name_ar']),
]


class Command(BaseCommand):
    help = """"Imports field translation to DB
    usage eg: `python manage.py migrate_translations translation_dumps_03-12-2018`
    """

    def add_arguments(self, parser):
        parser.add_argument('dir')

    def handle(self, *args, **options):
        self.stdout.write("-- Importing translations...")
        if not options.get('dir'):
            self.stdout.write("ERROR: no translation dump dir specified")
            return
        for file, klass, fields in FILES_CLASSES_FIELDS:
            with open('./{}/{}'.format(options['dir'], file)) as objs:
                objects = json.loads(objs.read())
                for o in objects:
                    try:
                        instance = klass.objects.get(pk=o['pk'])
                        for field in fields:
                            setattr(instance, field, o['fields'][field])
                        instance.save()
                    except klass.DoesNotExist:
                        pass
