import os
import json
import shutil

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.conf import settings

from country.models import Country
from country.models import MapFile
from pathlib import Path
from datetime import datetime


class Command(BaseCommand):
    help = "Remove unused features from geojson."

    def add_arguments(self, parser):
        parser.add_argument('code', nargs='*', type=str)

    def handle(self, *args, **options):
        country_code = options['code']

        if not country_code:
            self.stdout.write('No country code provided')
            return

        country_code = country_code[0].lower()

        try:
            c = Country.objects.get(code=country_code.upper())
        except ObjectDoesNotExist:
            self.stdout.write('Selected country does not exist')
            return

        map_file = MapFile.objects.filter(country_id=c.id).order_by('created').last()
        if not map_file:
            self.stdout.write('Selected country does not have an associated MapFile')
            return

        self.stdout.write('Removing unused features from {} geojson'.format(c.name))
        with open(os.path.join(settings.MEDIA_ROOT, '{}'.format(map_file.map_file)), encoding="utf-8") as f:
            json_content = json.load(f)

        level = c.map_data['first_sub_level']['admin_level']
        json_content['features'] = [fe for fe in json_content['features']
                                    if fe['properties']['admin_level'] == level]
        folder = os.path.join(settings.MEDIA_ROOT, 'processed_maps/')
        Path(folder).mkdir(parents=True, exist_ok=True)
        filename = '{}_slim.geojson'.format(country_code)
        with open(os.path.join(folder, filename), 'w') as out:
            json.dump(json_content, out)
        slim = os.path.join(folder, filename)
        static_name = '{}.json'.format(country_code)
        static_maps = os.path.join(settings.STATIC_ROOT, 'country-geodata')
        final_destination = os.path.join(static_maps, static_name)
        if os.path.isfile(final_destination):
            backup = os.path.join(settings.MEDIA_ROOT, 'topojson-backups',
                                  '{}-{}'.format(str(datetime.now()), static_name))
            shutil.move(final_destination, backup)
        os.system("mapshaper {} -o {} format=topojson".format(slim, final_destination))
