from __future__ import unicode_literals

from django.core.management.base import BaseCommand
import pprint as pp
import json
from project.models import UNICEFSector, RegionalPriority, InnovationCategory, CPD, Phase, TechnologyPlatform, \
    HardwarePlatform, NontechPlatform, PlatformFunction
from country.models import Currency


class Command(BaseCommand):
    help = 'Generates test data in the DB based on it the input JSON'
    json_path = 'project/static-json/taxonomies.json'

    data_model_map = {
        'UNICEF Sector': UNICEFSector,
        'Regional Priorities': RegionalPriority,
        'UNICEF Innovation Categories': InnovationCategory,
        'In Country programme document (CPD) and annual work plan?': CPD,
        'Phase of Initiative': Phase,
        'Software Platform(s)': TechnologyPlatform,
        'Hardware Platform(s)/Physical Product(s)': HardwarePlatform,
        'Non-Technology Platform(s)/Programme Innovation(s) and Non-Technology Platform(s)': NontechPlatform,
        'Function(s) of Platform': PlatformFunction
    }

    nonmodel_blocks = {
        'Links to website/Current Documentation',
        'Partner Type'
    }

    def add_arguments(self, parser):
        parser.add_argument('input_json', type=str)

    def parse_csv(self, file_path):  # Optional, better keep it
        from csv import reader
        with open(file_path) as csvfile:
            csv_reader = reader(csvfile, delimiter=',')
            column_names = next(csv_reader)
            pp.pprint(f'Columns: {column_names}')
            data = dict()
            for i, column in enumerate(column_names):
                splitted = column.split('- ')
                if len(splitted) == 2:
                    column_number = int(splitted[0].strip())
                    column_name = splitted[1].strip().replace('\n', '')
                else:
                    column_name = column.strip()
                    column_number = 0
                data[i] = {
                    'number': column_number,
                    'name': column_name,
                    'values': list()
                }
            for row in csv_reader:
                self.stdout.write(f'Read: {row}')
                for index in data:
                    if row[index] and data[index]['name'] == 'Currency':
                        data[index]['values'].append({'code': row[index], 'name': row[index - 1]})
                    elif row[index]:
                        data[index]['values'].append(row[index])
            data.pop(5)
            with open(self.json_path, 'w', encoding='utf-8') as ofile:
                json.dump({data[x]['name']: data[x]['values'] for x in data}, ofile, indent=4)

    @staticmethod
    def read_input_json(input_file):
        with open(input_file, 'r') as f:
            return json.load(f)

    @staticmethod
    def fill_named_model(data, model):
        for entry in data:
            _, created = model.objects.get_or_create(name=entry)
            pp.pprint(f'{entry}, created: {created}')

    @staticmethod
    def fill_currencies(data):
        for currency in data:
            curr, created = Currency.objects.update_or_create(
                code=currency['code'], defaults={'name': currency['name']})
            pp.pprint(f'{currency["name"]}, created: {created}')

    def handle(self, *args, **options):
        pp.pprint('Parsing input data')
        data = self.read_input_json(options.get('input_json'))

        for block_name in data:
            if block_name in self.data_model_map:
                self.fill_named_model(data[block_name], self.data_model_map[block_name])
            elif block_name == 'Currency':
                self.fill_currencies(data[block_name])
            elif block_name in self.nonmodel_blocks:
                pp.pprint(f"Warning: need to check {block_name} by hand as it's non-model")
            else:
                pp.pprint(f"Warning: unhandled block name: {block_name}")
