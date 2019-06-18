from django.utils.translation import ugettext_lazy as _


SEARCH_FILTERS = [
  {
    'name': 'project_name',
    'displayName': _('Project name'),
    'value': True
  },
  {
    'name': 'location',
    'displayName': _('Location'),
    'value': False
  },
  {
    'name': 'technology_platform',
    'displayName': _('Technology platform'),
    'value': False
  },
  {
    'name': 'organisation',
    'displayName': _('Organization'),
    'value': False
  },
  {
    'name': 'all',
    'displayName': _('Search in all'),
    'value': False
  }
]
