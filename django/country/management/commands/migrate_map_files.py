import json

from django.core.management.base import BaseCommand
from country.models import MapFile

FILENAME = 'countries_mapfiles.json'


class Command(BaseCommand):
    help = "Imports map files of countries"

    def handle(self, *args, **options):
        self.stdout.write("-- Importing map files...")
        with open('./{}'.format(FILENAME)) as countries:
            countries = json.load(countries)
            for c in countries:
                if MapFile.objects.filter(country_id=c['fields']['country']).exists():
                    mf = MapFile.objects.filter(country_id=c['fields']['country']).last()
                else:
                    mf = MapFile.objects.create(country_id=c['fields']['country'])
                mf.map_file.file.name = c['fields']['map_file']
                mf.save()
