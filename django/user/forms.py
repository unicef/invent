from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from core.utils import send_mail_wrapper
from django.utils.translation import ugettext_lazy as _


class PasswordHTMLEmailResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        send_mail_wrapper(email_type="password_reset",
                          subject=_(f"Your {settings.PROJECT_NAME} password has been reset"),
                          to=to_email,
                          language=context['user'].userprofile.language,
                          context=context)
