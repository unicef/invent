from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class EmailEndingValidator(RegexValidator):
    regex = r'(unicef.org|pulilab.com)$'
    message = _('Incorrect email address.')
