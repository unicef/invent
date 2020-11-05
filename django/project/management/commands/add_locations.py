from __future__ import unicode_literals

import pprint as pp
from django.core.management.base import BaseCommand

from country.models import RegionalOffice, Country, CountryOffice
from project.data_files.mappings import mappings, countries_not_matched, ro


class Command(BaseCommand):
    help = 'Generates data in the DB'

    def handle(self, *args, **options):
        pp.pprint('Create regional offices')
        for name in ro:
            RegionalOffice.objects.get_or_create(name=name)

        pp.pprint('Create missing countries')
        for name, code in countries_not_matched.items():
            Country.objects.get_or_create(name=name, code=code)

        pp.pprint('Create UNICEF offices')
        for unicef_office, regional_office, city, country_name, region in mappings:
            try:
                country = Country.objects.get(name__icontains=country_name)
            except Country.MultipleObjectsReturned:
                country = Country.objects.get(name=country_name)

            CountryOffice.objects.create(
                name=unicef_office,
                region=[y for x, y in Country.UNICEF_REGIONS].index(region),
                regional_office=RegionalOffice.objects.get(name=regional_office),
                city=city,
                country=country
            )
