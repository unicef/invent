import os
import shutil
import json

from django.core.management.base import BaseCommand
from django.conf import settings

import geodata_config
from country.models import Country
from project.models import Project


class Command(BaseCommand):
    help = "Imports geodata of countries from Mapzen."

    def handle(self, *args, **options):
        self.stdout.write("-- Importing geodata to the database...")
        for folder in os.listdir(settings.GEOJSON_TEMP_DIR):
            geodata = {}
            for filename in geodata_config.ADMIN_LEVELS_TO_IMPORT:
                with open(os.path.join(settings.GEOJSON_TEMP_DIR, folder, "topojson_" + filename)) as f:
                    content = f.read()
                    json_content = json.loads(content)
                    geodata[filename.strip(".geojson")] = json_content
            country, created = Country.objects.get_or_create(name=folder)
            country.geodata = geodata

            try:
                for geom in geodata['admin_level_2']['objects']['admin_level_2']['geometries']:
                    try:
                        country.code = geom['properties']['ISO3166-1']
                        break
                    except KeyError:
                        country.code = geom['properties']['ISO3166-1:alpha2']
            except Exception:
                if country.name == 'the-gambia':
                    country.code = 'GM'
                elif country.name == 'bangladesh':
                    country.code = 'BD'
                elif country.name == 'malawi':
                    country.code = 'MW'
                elif country.name == 'uzbekistan':
                    country.code = 'UZ'
                elif country.name == 'india':
                    country.code = 'IN'
                elif country.name == 'togo':
                    country.code = 'TG'
                elif country.name == 'azerbaijan':
                    country.code = 'AZ'

            finally:
                if not country.code:
                    country.code = "NULL"

                country.save()

            self.stdout.write("{} imported.".format(country.name))

        self.stdout.write("-- Writing Project Public IDs based on country codes...")
        for p in Project.objects.all():
            p.save()

        self.stdout.write("-- Removing temporary files...")
        shutil.rmtree(settings.GEOJSON_TEMP_DIR)
        self.stdout.write("-- Import is done!")
