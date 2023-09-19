from django.utils.translation import gettext_lazy as _

REVIEWER_QUESTIONS = {
    'psa': {'name': _('Problem Statement Alignment'),
            'text': _(
                'Which problem statement(s) (if any) does this project address across the relevant portfolio(s)?'),
            'text_bold': (''),
            'guidance': _('Please select from the list below the problem statement(s) that this project substantially '
                          'addresses. While many projects will touch on multiple problem statements, please limit '
                          'selection to the 1-2 problem statements that are most relevant'),
            'guidance_bold': (''),
            },
    'rnci': {'name': _('Reach: Number of Children Impacted'),
             'text': _('How many children could this innovation potentially reach globally in the next 12 months?  '),
             'text_bold': (''),
             'guidance': _(
                 '1 – Less than one million children\n3 – Tens of millions of children\n5 – Hundreds of millions of '
                 'children across multiple continents'),
             'guidance_bold': (''),
             },
    'ratp': {'name': _('Reach: Addressing Target Populations'),
             'text': _('Does this innovation reduce inequity by addressing populations affected by extreme poverty, '
                       'conflict, discrimination, exclusion, or other factors?'),
             'text_bold': (''),
             'guidance': _(
                 '1 - This initiative does not at all address populations affected by extreme poverty, conflict, '
                 'discrimination, exclusion, or other factors driving inequity \n3 - This initiative somewhat addresses'
                 ' populations affected by extreme poverty, conflict, discrimination, exclusion, or other factors '
                 'driving inequity, but this is not the target population \n5 - This initiative targets populations '
                 'affected by extreme poverty, conflict, discrimination, exclusion, or other factors driving inequity'),
             'guidance_bold': (''),
             },
    'ra': {'name': _('Risk Assessment'),
           'text': _(
               'What are the perceived risk levels associated with the initiative? This could be in terms of e.g.'
               'personnel, reputational, financial and data privacy risks.'),
           'text_bold': _('NOTE: A score of 1 indicates HIGHEST risk.'),
           'guidance': _(
               '1 - SIGNIFICANT RISKS that have not yet been adequately reduced or mitigated'
               '3 - risks identified, but appropriate mitigations are in place'
               '5 - NO MAJOR RISKS identified'),
           'guidance_bold': _('Note: Please use the open response box below to include any additional context about the'
                              ' nature of the risks associated with this initiative.'),
           },
    'ee': {'name': _('Evidence of Effectiveness'),
           'text': _('To what extent is there evidence that the innovation is having intended impact for children?'),
           'text_bold': (''),
           'guidance': _(
               '1 – no evidence presented\n3 – some evidence presented, but either further time or data required\n'
               '5 – strong evidence that innovation has potential to accelerate UNICEF results'),
           'guidance_bold': (''),
           'type': 'Select',
           },
    'nst': {'name': _('Newness of Solution (Tool)'),
            'text': _('How new is the solution or tool this initiative employs?'),
            'text_bold': _('NOTE: The purpose of this score is descriptive, not evaluative; higher score is not '
                           'considered more advantageous in portfolio review process.'),
            'guidance': _('1 – There is an existing solution and assets ({zero_percent_change})\n'
                        '3 – Existing solution needs to be evolved in a meaningful way for e.g. new context or users'
                        ' ({fifty_percent_change})\n'
                        '5 – No existing solution. New products, capabilities and assets needs to be developed\n'
                        ' ({hundred_percent_change})').format(zero_percent_change="0% change",
                                                            fifty_percent_change="50% change",
                                                            hundred_percent_change="100% change a.k.a. new solution"),
            'guidance_bold': (''),
            },
    'nc': {'name': _('Newness of Challenge'),
           'text': _('How new is the challenge or problem this initiative addresses?'),
           'text_bold': _('NOTE: The purpose of this score is descriptive, not evaluative; higher score is not '
                          'considered more advantageous in portfolio review process.'),
           'guidance': _(
               '1 - An existing problem/ challenge/ users that UNICEF is tackling or servicing in a meaningful way and'
               ' has a significant amount of experience in\n 3 - A moderately new problem or challenge that UNICEF has'
               ' some experience tackling\n5 - A completely new problem that UNICEF has not yet tackled or has'
               ' neglected servicing'),
           'guidance_bold': (''),
           },
    'ps': {'name': _('Path to Scale'),
           'text': _('Does this innovation have a sustainable and scalable business or operating model?'),
           'text_bold': (''),
           'guidance': _('1 – No obvious path to sustainable scale for UNICEF and partners\n'
                         '3 – Potential scaling / sustainability models exist, but need further refinement and '
                         'testing\n'
                         '5 – Robust business model for scale is in place'),
           'guidance_bold': (''),
           },
    # Manager questions - no real reason to separate these from the rest
    'impact': {'name': _('Impact'),
               'text': _(
                   'Composite score based on Reach: Number of Children Impacted, in the context of target population '
                   'size provided by project team; Reach: Addressing Target Populations; Evidence of Effectiveness; '
                   'Problem Statement Alignment'),
               'text_bold': (''),
               'guidance': _(
                   'When assigning composite impact score, consider both the breadth and depth of the reach, as well as'
                   ' the severity of the problem that the initiative addresses.'),
               'guidance_bold': (''),
               },
    'scale_phase': {'name': _('Scale Phase'),
                    'text': _('What stage of scale is this initiative currently in?'),
                    'text_bold': (''),
                    'guidance': _('Consult IDIA scale phases for guidance.'),
                    'guidance_bold': (''),
                    },
    'overal_summary': {'name': _('Overall Summary'),
                       'text': (''),
                       'text_bold': (''),
                       'guidance': _('Please provide your overall thoughts on this initiative, with a particular focus'
                                     ' on any key points not covered in your previous answers.'),
                       'guidance_bold': (''),
                       },
}
