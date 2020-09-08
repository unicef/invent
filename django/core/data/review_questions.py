from django.utils.translation import ugettext_lazy as _

standardChoices = [
    {'label': _('1'),
     'value': 1},
    {'label': _('2'),
     'value': 2},
    {'label': _('3'),
     'value': 3},
    {'label': _('4'),
     'value': 4},
    {'label': _('5'),
     'value': 5}
]

REVIEWER_QUESTIONS = {
    'psa': {'ref_id': 'psa',
            'name': _('Problem Statement Alignment'),
            'text': _(
                'Which problem statement(s) (if any) does this project address across the relevant portfolio(s)?'),
            'guidance': _('Please select from the list below the problem statement(s) that this project substantially '
                          'addresses. While many projects will touch on multiple problem statements, please limit selection '
                          'to the 1-2 problem statements that are most relevant'),
            'type': 'ProblemStatement',
            'choices': None
            },
    'rnci': {'ref_id': 'rnci',
             'name': _('Reach: Number of Children Impacted'),
             'text': _('How many children could this innovation potentially reach globally?'),
             'guidance': _(
                 '1 – Less than one million children\n3 – Tens of millions of children\n5 – Hundreds of millions of '
                 'children across multiple continents'),
             'type': 'Select',
             'choices': standardChoices,
             },
    'ratp': {'ref_id': 'ratp',
             'name': _('Reach: Addressing Target Populations'),
             'text': _('Does this innovation reduce inequities?'),
             'guidance': _(
                 '1 – This initiative does not address UNICEF’s equity agenda at all\n3 – This initiative somewhat '
                 'addresses UNICEF’s equity agenda\n5 – This initiative is directly addressing UNICEF’s equity'
                 ' agenda by targeting the most vulnerable or difficult to reach populations'),
             'type': 'Select',
             'choices': standardChoices
             },
    'ra': {'ref_id': 'ra',
           'name': _('Risk Assessment'),
           'text': _(
               'What are the perceived risk levels associated with the project/ initiative? This could be in terms of '
               'e.g. personnel, reputation, financial and data privacy risks.'),
           'guidance': _(
               '1 – no major risks identified\n3 – risks identified, but appropriate mitigations are in place\n'
               '5 – significant risks that have not yet been adequately reduced or mitigated\n\n'
               'Note: Please use the open response box below to include any additional context about the nature of '
               'the risks associated with this initiative.'),
           'type': 'SelectExtended',
           'choices': standardChoices,
           'answer_text': []
           },
    'ee': {'ref_id': 'ee',
           'name': _('Evidence of Effectiveness'),
           'text': _('To what extent is there evidence that the innovation is having intended impact for children?'),
           'guidance': _(
               '1 – no evidence presented\n3 – some evidence presented, but either further time or data required\n'
               '5 – strong evidence that innovation has potential to accelerate UNICEF results'),
           'type': 'Select',
           'choices': standardChoices,
           },
    'nst': {'ref_id': 'nst',
            'name': _('Newness of Solution (Tool)'),
            'text': _('How new is the solution or tool this project / initiative employs?'),
            'guidance': _('1 – There is an existing solution and assets (0% change)\n'
                          '3 – Existing solution needs to be evolved in a meaningful way for e.g. new context or users'
                          ' (50% change)\n'
                          '5 – No existing solution. New products, capabilities and assets needs to be developed\n'
                          ' (100% change a.k.a. new solution)'),
            'type': 'Select',
            'choices': standardChoices,
            },
    'nc': {'ref_id': 'nc',
           'name': _('Newness of Challenge'),
           'text': _('How new is the challenge or problem this project / initiative addresses?'),
           'guidance': _(
               '1 – An existing problem/ challenge/ users that UNICEF is tackling or servicing in a meaningful way'
               ' and has a significant amount of experience in\n'
               '3 – A moderately new problem or challenge that UNICEF has some experience tackling\n'
               '5 – A completely new problem that UNICEF has not yet tackled or has neglected servicing'),
           'type': 'Select',
           'choices': standardChoices,
           },
    'ps': {'ref_id': 'ps',
           'name': _('Path to Scale'),
           'text': _('Does this innovation have a sustainable and scalable business or operating model?'),
           'guidance': _('1 – No obvious path to sustainable scale for UNICEF and partners\n'
                         '3 – Potential scaling / sustainability models exist, but need further refinement and testing\n'
                         '5 – Robust business model for scale is in place'),
           'type': 'Select',
           'choices': standardChoices,
           },
}

MANAGER_QUESTIONS = {
    'm_i': {'ref_id': 'm_i',
            'name': _('Impact'),
            'text': _(
                'Composite score based on Reach: Number of Children Impacted; Reach: Addressing Target Populations; '
                'Evidence of Effectiveness'),
            'guidance': _(''),
            'type': 'Select',
            'keys': []
            },
    'm_sp': {'ref_id': 'm_sp',
             'name': _('Scale Phase'),
             'text': _('What stage of scale is this project / initiative currently in?'),
             'guidance': _(''),
             'type': 'Select',
             'choices': [
                 {'label': _('1 - Ideation'),
                  'value': 1},
                 {'label': _('2 - Research & Development'),
                  'value': 2},
                 {'label': _('3 - Proof of Concept'),
                  'value': 3},
                 {'label': _('4 - Transition to Scale'),
                  'value': 4},
                 {'label': _('5 - Scaling'),
                  'value': 5},
                 {'label': _('6 - Sustainable Scale'),
                  'value': 6}
             ],
             }
}
