from django.utils.translation import ugettext_lazy as _


AXIS_DATA = {
    'labels': [
        {'id': 'groundwork',
         'name': _('Groundwork')},
        {'id': 'partnerships',
         'name': _('Partnership')},
        {'id': 'financialHealth',
         'name': _('Financial health')},
        {'id': 'technologyAndArchitecture',
         'name': _('Technology & Architecture')},
        {'id': 'operations',
         'name': _('Operations')},
        {'id': 'monitoringAndEvaluation',
         'name': _('Monitoring & Evaulation')}
    ],
    'data': []
}

DOMAIN_DATA = {
    'labels': [
        _('Groundwork'),
        _('Partnerships'),
        _('Financial health'),
        _('Technology & Architecture'),
        _('Operations'),
        _('Monitoring & evaluation')
    ],
    'groundwork': {
        'labels': [
            _('Parameters of scale'),
            _('Contextual environment'),
            _('Scientific basis')
        ],
        'data': []
    },
    'partnerships': {
        'labels': [
            _('Strategic engagement'),
            _('Partnership sustainability')
        ],
        'data': []
    },
    'financialHealth': {
        'labels': [
            _('Financial management'),
            _('Financial model')
        ],
        'data': []
    },
    'technologyAndArchitecture': {
        'labels': [
            _('Data'),
            _('Interoperability'),
            _('Adaptability')
        ],
        'data': []
    },
    'operations': {
        'labels': [
            _('Personnel'),
            _('Training & support'),
            _('Outreach & sanitization'),
            _('Contingency planning')
        ],
        'data': []
    },
    'monitoringAndEvaluation': {
        'labels': [
            _('Process monitoring'),
            _('Evaluation reach')
        ],
        'data': []
    }
}


CHART_DATA = {'axisData',
              'domainData'}
