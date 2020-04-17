from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import DefaultAccountAdapter
from rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.sites.models import Site

from core.utils import send_mail_wrapper
from azure.views import AzureOAuth2Adapter
from .models import UserProfile

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery # noqa


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    ACTIVATE_BASE_URL = 'http://' + Site.objects.get(id=settings.SITE_ID).domain + '/'

    def send_mail(self, template_prefix, email, context):
        activate_url = self.ACTIVATE_BASE_URL + \
            'en/-/email-confirmation/' + context['key']

        context.update({"activate_url": activate_url})

        send_mail_wrapper(subject="Welcome to the T4D & Innovation Inventory Portal",
                          email_type='email_confirmation_signup_message',
                          to=email,
                          language=context['user'].userprofile.language,
                          context=context)


class AzureLogin(SocialLoginView):
    adapter_class = AzureOAuth2Adapter
    callback_url = settings.SOCIALACCOUNT_CALLBACK_URL
    client_class = OAuth2Client


class MyAzureAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        request.sociallogin = sociallogin

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        try:
            data = {
                "user": user,
            }
            UserProfile.objects.get_or_create(name=sociallogin.account.extra_data['displayName'], defaults=data)
        except Exception:
            pass
        return user
