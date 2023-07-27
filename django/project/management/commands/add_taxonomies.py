from __future__ import unicode_literals

from django.core.management.base import BaseCommand
import pprint as pp
import json
from project.models import UNICEFSector, RegionalPriority, InnovationCategory, CPD, TechnologyPlatform, \
    HardwarePlatform, NontechPlatform, PlatformFunction, ISC, InnovationWay, Stage
from country.models import Currency


class Command(BaseCommand):
    help = 'Generates test data in the DB based on it the input JSON'
    json_path = 'project/data_files/taxonomies.json'

    data_model_map = {
        'UNICEF Sector': UNICEFSector,
        'Regional Priorities': RegionalPriority,
        'UNICEF Innovation Categories': InnovationCategory,
        'In Country programme document (CPD) and annual work plan?': CPD,
        'Phase of Initiative': Stage,
        'Software Platform(s)': TechnologyPlatform,
        'Hardware Platform(s)/Physical Product(s)': HardwarePlatform,
        'Non-Technology Platform(s)/Programme Innovation(s) and Non-Technology Platform(s)': NontechPlatform,
        'Function(s) of Platform': PlatformFunction,
        "Information Security Classification as per UNICEF's Classi Tool": ISC,
        "If this is an innovation initiative, in which way is it innovative?": InnovationWay
    }

    nonmodel_blocks = {
        'Links to website/Current Documentation',
        'Partner Type'
    }

    @staticmethod
    def read_input_json(input_file):
        with open(input_file, 'r') as f:
            return json.load(f)

    @staticmethod
    def fill_named_model(data, model):
        for entry in data:
            _, created = model.objects.get_or_create(name=entry)
            if created:
                pp.pprint(f'{entry} created')

    @staticmethod
    def fill_currencies(data):
        for currency in data:
            curr, created = Currency.objects.update_or_create(
                code=currency['code'], defaults={'name': currency['name']})
            pp.pprint(f'{currency["name"]}, created: {created}')

    def handle(self, *args, **options):
        if options['verbosity'] == 0:
            pp.pprint = lambda *x: x

        pp.pprint('Parsing input data')
        data = self.read_input_json(self.json_path)

        for block_name in data:
            if block_name in self.data_model_map:
                self.fill_named_model(data[block_name], self.data_model_map[block_name])
            elif block_name == 'Currency':
                self.fill_currencies(data[block_name])
            elif block_name in self.nonmodel_blocks:
                pp.pprint(f"Warning: need to check {block_name} by hand as it's non-model")
            else:  # pragma: no cover
                pp.pprint(f"Warning: unhandled block name: {block_name}")
