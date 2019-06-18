import json

from django.core.management.base import BaseCommand
from country.models import Country

FILENAME = 'countries-12-11-2018.json'


class Command(BaseCommand):
    help = "Imports map data of countries"

    def handle(self, *args, **options):
        self.stdout.write("-- Importing map_data...")
        with open('./{}'.format(FILENAME)) as countries:
            countries = json.load(countries)
            for c in countries:
                try:
                    country, created = \
                        Country.objects.get_or_create(code=c['fields']['code'],
                                                      defaults={'name': c['fields']['name'],
                                                                'name_en': c['fields']['name_en'],
                                                                'region': c['fields']['region'],
                                                                'map_data': c['fields']['map_data'],
                                                                'lat': c['fields']['lat'],
                                                                'lon': c['fields']['lon']})
                    if not created:
                        country.name = c['fields']['name']
                        country.name_en = c['fields']['name_en']
                        country.region = c['fields']['region']
                        country.map_data = c['fields']['map_data']
                        country.lat = c['fields']['lat']
                        country.lon = c['fields']['lon']
                        country.save()
                except KeyError:
                    raise
