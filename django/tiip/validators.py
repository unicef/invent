from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class EmailEndingValidator(RegexValidator):
    regex = settings.EMAIL_VALIDATOR_REGEX
    message = _('Incorrect email address.')
