from django.utils.translation import ugettext_lazy as _


LANDING_PAGE_DEFAULTS = {
    'name': 'WHO',
    'code': 'who',
    'logo': False,
    'cover': '',
    'cover_text': _('The Digital Health Atlas is a WHO global technology registry platform aiming to strengthen the '
                    'value and impact of digital health investments, improve coordination, and facilitate '
                    'institutionalization and scale.'),
    'footer_title': '',
    'permanent_footer': _('The DHA is a global public good overseen by the World Health Organization. '
                          'The DHA benefits from a diversity of contributions, including support from WHO'
                          ' Reproductive Health and Research, PATH, Digital Square, USAID, UN Foundation,'
                          ' UNFPA, JHU Global mHealth Initiative, mPowering, and the Digital Health and'
                          ' Interoperability Working Group, and was developed to strengthen coordination'
                          ' of investments into deliberate, harmonized, interoperable digital health systems'),
    'footer_text': '',
    'default_partners': [],
    'partner_logos': []
}
