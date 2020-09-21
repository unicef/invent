from django.utils.translation import ugettext_lazy as _


REVIEWER_QUESTIONS = {
    'psa': {'name': _('Problem Statement Alignment'),
            'text': _(
                'Which problem statement(s) (if any) does this project address across the relevant portfolio(s)?'),
            'guidance': _('Please select from the list below the problem statement(s) that this project substantially '
                          'addresses. While many projects will touch on multiple problem statements, please limit '
                          'selection to the 1-2 problem statements that are most relevant'),
            },
    'rnci': {'name': _('Reach: Number of Children Impacted'),
             'text': _('How many children could this innovation potentially reach globally?'),
             'guidance': _(
                 '1 – Less than one million children\n3 – Tens of millions of children\n5 – Hundreds of millions of '
                 'children across multiple continents'),
             },
    'ratp': {'name': _('Reach: Addressing Target Populations'),
             'text': _('Does this innovation reduce inequities?'),
             'guidance': _(
                 '1 – This initiative does not address UNICEF’s equity agenda at all\n3 – This initiative somewhat '
                 'addresses UNICEF’s equity agenda\n5 – This initiative is directly addressing UNICEF’s equity'
                 ' agenda by targeting the most vulnerable or difficult to reach populations'),
             },
    'ra': {'name': _('Risk Assessment'),
           'text': _(
               'What are the perceived risk levels associated with the project/ initiative? This could be in terms of '
               'e.g. personnel, reputation, financial and data privacy risks.'),
           'guidance': _(
               '1 – no major risks identified\n3 – risks identified, but appropriate mitigations are in place\n'
               '5 – significant risks that have not yet been adequately reduced or mitigated\n\n'
               'Note: Please use the open response box below to include any additional context about the nature of '
               'the risks associated with this initiative.'),
           },
    'ee': {'name': _('Evidence of Effectiveness'),
           'text': _('To what extent is there evidence that the innovation is having intended impact for children?'),
           'guidance': _(
               '1 – no evidence presented\n3 – some evidence presented, but either further time or data required\n'
               '5 – strong evidence that innovation has potential to accelerate UNICEF results'),
           'type': 'Select',
           },
    'nst': {'name': _('Newness of Solution (Tool)'),
            'text': _('How new is the solution or tool this project / initiative employs?'),
            'guidance': _('1 – There is an existing solution and assets (0% change)\n'
                          '3 – Existing solution needs to be evolved in a meaningful way for e.g. new context or users'
                          ' (50% change)\n'
                          '5 – No existing solution. New products, capabilities and assets needs to be developed\n'
                          ' (100% change a.k.a. new solution)'),
            },
    'nc': {'name': _('Newness of Challenge'),
           'text': _('How new is the challenge or problem this project / initiative addresses?'),
           'guidance': _(
               '1 – An existing problem/ challenge/ users that UNICEF is tackling or servicing in a meaningful way'
               ' and has a significant amount of experience in\n'
               '3 – A moderately new problem or challenge that UNICEF has some experience tackling\n'
               '5 – A completely new problem that UNICEF has not yet tackled or has neglected servicing'),
           },
    'ps': {'name': _('Path to Scale'),
           'text': _('Does this innovation have a sustainable and scalable business or operating model?'),
           'guidance': _('1 – No obvious path to sustainable scale for UNICEF and partners\n'
                         '3 – Potential scaling / sustainability models exist, but need further refinement and '
                         'testing\n '
                         '5 – Robust business model for scale is in place'),
           },
    # Manager questions - no real reason to separate these from the rest
    'impact': {'name': _('Impact'),
               'text': _(
                   'Composite score based on Reach: Number of Children Impacted; Reach: Addressing Target Populations; '
                   'Evidence of Effectiveness'),
               'guidance': _(''),
               },
    'scale_phase': {'name': _('Scale Phase'),
                    'text': _('What stage of scale is this project / initiative currently in?'),
                    'guidance': _('1 - Ideation\n2 - Research & Development\n3 - Proof of Concept\n'
                                  '4 - Transition to Scale\n5 - Scaling\n6 - Sustainable Scale'),
                    }
}
