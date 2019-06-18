from django.utils.translation import ugettext_lazy as _

CATEGORIES = [
    {'id': 1,
     'name': _('About')},
    {'id': 2,
     'name': _('Introduction')}
]

SUB_CATEGORIES = [
    {'id': 11,
     'category': 1,
     'name': _('Foreword')},
    {'id': 12,
     'category': 1,
     'name': _('Acknowledgements')},
    {'id': 19,
     'category': 1,
     'name': _('Executive summary')},
    {'id': 20,
     'category': 1,
     'name': _('Acronyms and abbreviations')},
    {'id': 21,
     'category': 1,
     'name': _('Key terminology')},

    {'id': 22,
     'category': 2,
     'name': _('Background: scaling up mHealth')},
    {'id': 23,
     'category': 2,
     'name': _('The MAPS Toolkit')},
    {'id': 24,
     'category': 2,
     'name': _('How to use MAPS')}
]

THEMATIC_OVERVIEW = {
    'categories': CATEGORIES,
    'sub_categories': SUB_CATEGORIES
}
