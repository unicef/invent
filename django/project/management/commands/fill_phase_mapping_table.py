import json
from django.core.management.base import BaseCommand
from project.models import Phase, Stage


class Command(BaseCommand):
    help = """
    Fill phases mapping table
    """
    json_path = 'project/data_files/phase_mapping.json'
    py_path = 'project/data_files/phase_mapping_table.py'

    def handle(self, *args, **options):  # pragma: no cover
        with open(self.json_path, 'w+') as f:
            data = {}
            data['old_phases'] = list(Phase.objects.values('id', 'name'))
            data['new_phases'] = list(Stage.objects.values('id', 'name'))

            mapping = {
                'Preparation and Scoping': 'Opportunity and Ideation',
                'Analysis and Design': 'Preparation and Scoping',
                'Implementation Planning': 'Analysis and Design',
                'Developing or Adapting Solution': 'Implementation Planning',
                'Piloting and Evidence Generation': 'Developing or Adapting Solution',
                'Package and Advocacy': 'Piloting and Evidence Generation',
                'Deploying': 'Package and Advocacy',
                'Scaling Up': 'Deploying',
                'Handover or Complete': 'Scaling Up',
                'Discontinued': 'Discontinued'
            }
            id_map = {}

            for old, new in mapping.items():
                id_map[Phase.objects.get(name__icontains=old).id] = Stage.objects.get(name__icontains=new).id

            data['id_map'] = id_map

            json.dump(data, f, indent=4)

            with open(self.py_path, 'w') as py_file:
                py_file.write('ID_MAP = ')
                json.dump(id_map, py_file)

            self.stdout.write("Phase mapping success")
