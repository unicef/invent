import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from country.models import Country


class Command(BaseCommand):
    help = "Load default sub levels data from topojson."

    def add_arguments(self, parser):
        parser.add_argument('code', nargs='*', type=str)

    def manage_map(self, country):
        self.stdout.write('Loading defaults from {} topojson'.format(country.name))
        with open(os.path.join(settings.STATIC_ROOT, 'country-geodata', '{}.json'.format(country.code.lower()))) as f:
            json_content = json.load(f)

        # It's a dict with one key but we don't know the key name
        feature_keys = list(json_content['objects'].keys())[0]
        features = json_content['objects'][feature_keys]['geometries']
        first_sub_level = {
            'name': 'district',
            'elements': list(map(lambda x: {'name': x['properties'].get('name') or x['properties'].get('wof:name')},
                                 features))
        }
        country.map_data = {
            'first_sub_level': first_sub_level,
            'second_sub_level': {
                'name': '',
                'elements': []
            },
            'facilities': []
        }
        country.save()
        self.stdout.write('{} done'.format(country.name))

    def handle(self, *args, **options):
        country_code = options['code']

        if country_code:
            countries = Country.objects.filter(code=country_code[0].upper())
        else:
            countries = Country.objects.filter(map_data={})

        for country in countries:
            self.manage_map(country)
