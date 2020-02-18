from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.models import Site

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery # noqa
from core.utils import send_mail_wrapper


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    ACTIVATE_BASE_URL = 'http://' + Site.objects.get(id=settings.SITE_ID).domain + '/'

    def send_mail(self, template_prefix, email, context):
        activate_url = self.ACTIVATE_BASE_URL + \
            'en/-/email-confirmation/' + context['key']

        context.update({"activate_url": activate_url})

        send_mail_wrapper(subject="Welcome to the Digital Health Atlas",
                          email_type='email_confirmation_signup_message',
                          to=email,
                          language=context['user'].userprofile.language,
                          context=context)
