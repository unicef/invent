# coding=utf-8
from django.utils.translation import ugettext_lazy as _


AXIS = [
    {'id': 1,
     'name': _('Groundwork')},
    {'id': 2,
     'name': _('Partnership')},
    {'id': 3,
     'name': _('Financial Health')},
    {'id': 4,
     'name': _('Technology & Architecture')},
    {'id': 5,
     'name': _('Operations')},
    {'id': 6,
     'name': _('Monitoring & Evaluation')}
]

DOMAINS = [
    {'id': 1,
     'axis': 1,
     'sub_text': _('The articulation of the basic features of the scaling-up process, including the endgame '
                   'strategy, which will guide decision-making in other arenas'),
     'name': _('Parameters of Scale')},
    {'id': 2,
     'axis': 1,
     'sub_text': _('The assessment of the environmental elements that may facilitate or impede implementation of '
                   'mHealth in the setting or settings targeted for scaling up'),
     'name': _('Contextual environment')},
    {'id': 3,
     'axis': 1,
     'sub_text': 'The assessment of general and context-specific evidence supporting the innovation, in order to '
                 'identify whether there is a need for additional evaluation activities prior to scaling up '
                 'further',
     'name': _('Scientific basis')},

    {'id': 4,
     'axis': 2,
     'sub_text': 'The development of partnerships with external groups that contribute the skill sets, expertise, '
                 'services and/or other essential components needed for scaling up',
     'name': _('Strategic Engagement')},
    {'id': 5,
     'axis': 2,
     'sub_text': 'The establishment of mechanisms will help to sustain partnerships as new challenges emerge '
                 'during scaling up',
     'name': _('Partnership Sustainability')},

    {'id': 6,
     'axis': 3,
     'sub_text': 'The understanding, assessment and projection of costs that will be associated with scaling up '
                 'the mHealth product',
     'name': _('Financial Management')},
    {'id': 7,
     'axis': 3,
     'sub_text': 'The analysis of the value proposition for each stakeholder and the identification of revenue '
                 'streams capable of sustaining project activities',
     'name': _('Financial Model')},

    {'id': 8,
     'axis': 4,
     'sub_text': 'Efforts to ensure that a number of elements of the mHealth technology and system are appropriate '
                 'to data needs throughout all stages of the scaling-up process, including access, transmission, '
                 'storage and security',
     'name': _('Data')},
    {'id': 9,
     'axis': 4,
     'sub_text': 'The technology’s ability to work with other information systems and services within and across'
                 'organizations',
     'name': _('Interoperability')},
    {'id': 10,
     'sub_text': 'The extent to which various components of the product are able to accommodate improvements and '
                 'changes as needs shift throughout the scaling-up process',
     'axis': 4,
     'name': _('Adaptability')},

    {'id': 11,
     'axis': 5,
     'sub_text': 'Considerations surrounding the restructuring and expansion of human resources, including project '
                 'team members (staff and health workers) and leadership positions',
     'name': _('Personnel')},
    {'id': 12,
     'axis': 5,
     'sub_text': 'The availability of appropriate training activities to ensure that users have the necessary '
                 'skills and capacity required to support scaling up, and the presence of reliable assistance and '
                 'supervisory structures to address emerging issues while scaling up',
     'name': _('Training and Support')},
    {'id': 13,
     'axis': 5,
     'sub_text': 'Efforts to orient key stakeholder groups and raise awareness in targeted communities in order to '
                 'promote wider acceptance of the mHealth product and its scaling up',
     'name': _('Outreach and Sensitization')},
    {'id': 14,
     'axis': 5,
     'sub_text': 'Considerations and guidelines surrounding operational procedures to maintain the continuity of '
                 'use of the product in light of technical and programmatic obstacles',
     'name': _('Contingency Planning')},

    {'id': 15,
     'axis': 6,
     'sub_text': 'The routine monitoring of implementation fidelity and use of the product, and the use of these '
                 'data for the purposes of continuous improvement',
     'name': _('Process Monitoring')},
    {'id': 16,
     'axis': 6,
     'sub_text': 'Process in place to assess the product’s effects in relation to the health system, health '
                 'services and/or individuals’ health status, using rigorous and systematic research methods',
     'name': _('Evaluation Research')}
]
