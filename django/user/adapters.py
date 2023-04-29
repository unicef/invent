from allauth.account.utils import setup_user_email
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount, SocialApp

from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from rest_auth.registration.views import SocialLoginView
from django.conf import settings
from azure.views import AzureOAuth2Adapter
from .models import UserProfile
from country.models import Country

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery  # noqa


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    def validate_unique_email(self, email):  # pragma: no cover
        return email


class AzureLogin(SocialLoginView):
    adapter_class = AzureOAuth2Adapter
    callback_url = settings.SOCIALACCOUNT_CALLBACK_URL
    client_class = OAuth2Client


class MyAzureAccountAdapter(DefaultSocialAccountAdapter):  # pragma: no cover
    def save_user(self, request, sociallogin, form=None):
        u = sociallogin.user
        u.set_unusable_password()
        DefaultAccountAdapterCustom().populate_username(request, u)
        assert not sociallogin.is_existing
        user = sociallogin.user
        name = sociallogin.account.extra_data.get('displayName')
        job_title = sociallogin.account.extra_data.get('jobTitle')
        department = sociallogin.account.extra_data.get('department')
        country = sociallogin.account.extra_data.get('country')

        user_model = get_user_model()
        try:
            old_user = user_model.objects.filter(email=user.email).get()
        except user_model.DoesNotExist:
            user.save()
            sociallogin.account.user = user
            sociallogin.account.save()
            UserProfile.objects.create(
                user=user,
                name=name,
                account_type=UserProfile.DONOR,
                job_title=job_title,
                department=department,
                country=country
            )
            setup_user_email(request, user, sociallogin.email_addresses)
        else:
            sociallogin.account.user = old_user
            sociallogin.account.save()
            sociallogin.user = old_user
            if not old_user.userprofile.name:
                old_user.userprofile.name = name
                old_user.userprofile.job_title = job_title
                old_user.userprofile.department = department
                old_user.userprofile.save()

        return user

    def save_aad_users(self, azure_users):
        user_model = get_user_model()

        for azure_user in azure_users:
            email = azure_user['mail']
            display_name = azure_user['displayName']
            job_title = azure_user['jobTitle']
            department = azure_user['department']
            country_name = azure_user['country']
            social_account_uid = azure_user['id']

            # Get or create user
            try:
                user = user_model.objects.get(email=email)
            except user_model.DoesNotExist:
                user = user_model.objects.create(email=email, username=email)
                user.set_unusable_password()
                user.save()

            # Check if the user exists
            try:
                old_user = user_model.objects.filter(email=user.email).get()
            except user_model.DoesNotExist:
                # Get or create Country instance
                country, _ = Country.objects.get_or_create(name=country_name)

                # Update UserProfile
                UserProfile.objects.create(
                    user=user,
                    name=display_name,
                    account_type=UserProfile.DONOR,
                    job_title=job_title,
                    department=department,
                    country=country
                )
                # Here you can call the same setup_user_email function as in save_user method.
                # However, since it's not available in this scope, you can replace it with your email setup logic.
                # setup_user_email(request, user, sociallogin.email_addresses)
            else:
                # Get or create UserProfile
                user_profile, created = UserProfile.objects.get_or_create(user=old_user)

                if not user_profile.name:
                    user_profile.name = display_name
                    user_profile.job_title = job_title
                    user_profile.department = department

                    # Get or create Country instance
                    country, _ = Country.objects.get_or_create(name=country_name)
                    user_profile.country = country

                    user_profile.save()

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
