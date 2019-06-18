from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import ugettext, override

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery # noqa


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    ACTIVATE_BASE_URL = 'http://' + Site.objects.get(id=settings.SITE_ID).domain + '/'

    def send_mail(self, template_prefix, email, context):
        activate_url = self.ACTIVATE_BASE_URL + \
            'en/-/email-confirmation/' + context['key']
        profile = context['user'].userprofile
        html_template = loader.get_template("email/master-inline.html")

        with override(profile.language):
            html_message = html_template.render({"type": "email_confirmation_signup_message",
                                                 "language": profile.language,
                                                 "activate_url": activate_url})
            subject = ugettext("Welcome to the Digital Health Atlas")

        send_mail(
            subject=subject,
            message="",
            from_email=settings.FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message)
