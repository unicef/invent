from datetime import datetime
from typing import Dict, List, Tuple, Union

from django.conf import settings
from .data_files.phase_mapping_table import ID_MAP


def remove_keys(data_dict: Dict, keys: Union[List, Tuple]) -> Dict:
    for key in keys:
        if key in data_dict:
            data_dict.pop(key, None)
    return data_dict


def _migrate_phases_to_stages(data: Dict, modified: datetime):
    if 'phase' in data and not data.get('stages'):
        if str(data['phase']) in ID_MAP.keys():
            data["stages"] = [{
                "id": ID_MAP[str(data['phase'])],
                "date": modified.isoformat().replace("+00:00", "Z"),
            }]
        data.pop('phase')
        return True


def migrate_project_phases(project):
    if settings.MIGRATE_PHASES:
        if not ID_MAP or not isinstance(ID_MAP, dict):  # pragma: no cover
            print('ID MAPPING has not been completed, please run `manage.py fill_phase_mapping_table` first')
        else:
            if any([_migrate_phases_to_stages(project.data, project.modified), 
                    _migrate_phases_to_stages(project.draft, project.modified)]):
                project.save(update_fields=['draft', 'data'])
