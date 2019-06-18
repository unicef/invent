from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import override, ugettext


class PasswordHTMLEmailResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        html_template = loader.get_template("email/master-inline.html")
        profile = context['user'].userprofile
        context.update({"type": "password_reset", "language": profile.language, "email": to_email})

        with override(profile.language):
            html_message = html_template.render(context)
            subject = ugettext("Your Digital Health Atlas password has been reset")

        send_mail(
            subject=subject,
            message="",
            from_email=settings.FROM_EMAIL,
            recipient_list=[to_email],
            html_message=html_message)
