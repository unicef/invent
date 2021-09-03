from typing import Dict, List, Tuple, Union

from django.conf import settings
from .data_files.phase_mapping_table import ID_MAP


def remove_keys(data_dict: Dict, keys: Union[List, Tuple]) -> Dict:
    for key in keys:
        if key in data_dict:
            data_dict.pop(key, None)
    return data_dict


def _migrate_phases_to_stages(data: Dict):
    if 'phase' in data and not data.get('stages'):
        if str(data['phase']) in ID_MAP.keys():
            data["stages"] = [{
                "id": ID_MAP[str(data['phase'])]
            }]
        data.pop('phase')
        return True


def migrate_project_phases(project):
    if settings.MIGRATE_PHASES:
        if not ID_MAP or not isinstance(ID_MAP, dict):  # pragma: no cover
            print('ID MAPPING has not been completed, please run `manage.py fill_phase_mapping_table` first')
        else:
            if any([_migrate_phases_to_stages(project.data), 
                    _migrate_phases_to_stages(project.draft)]):
                project.save(update_fields=['draft', 'data'])


def project_status_change(version_1, version_2) -> dict:
    return dict(
        published=not version_1.published and version_2.published,
        unpublished=not version_2.published and version_1.published,
        data_changed=version_1.data != version_2.data,
        name_changed=version_1.name != version_2.name,
    )


def project_status_change_str(status_dict: dict) -> str:  # pragma: no cover
    changes = list()
    if status_dict.get('published'):
        changes.append('published')
    if status_dict.get('unpublished'):
        changes.append('unpublished')
    if status_dict.get('data_changed'):
        changes.append('data was changed')
    if status_dict.get('name_changed'):
        changes.append('name was changed')

    return ', '.join(changes)
