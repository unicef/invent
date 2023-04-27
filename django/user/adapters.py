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
            # Update the following line to include job_title and department when creating a UserProfile
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
                old_user.userprofile.job_title = job_title  # Add this line to update the job_title
                old_user.userprofile.department = department  # Add this line to update the department
                old_user.userprofile.save()

        return user

    # def save_users_from_azure(self, azure_users):
    #     user_model = get_user_model()

    #     for azure_user in azure_users:
    #         email = azure_user['mail']
    #         display_name = azure_user['displayName']
    #         social_account_uid = azure_user['id']

    #         try:
    #             old_user = user_model.objects.filter(email=email).get()
    #         except user_model.DoesNotExist:
    #             # Create a new user with the information from Azure
    #             user = user_model(email=email, username=email)
    #             user.set_unusable_password()
    #             user.save()

    #             # Create social account for the user
    #             social_account = self.get_social_account(user, social_account_uid)
    #             social_account.save()

    #             # Create UserProfile
    #             UserProfile.objects.create(user=user, name=display_name, account_type=UserProfile.DONOR)
    #         else:
    #             # Update social account for the existing user
    #             social_account = self.get_social_account(old_user, social_account_uid)
    #             social_account.save()

    #             # Update user profile if necessary
    #             if not old_user.userprofile.name:
    #                 old_user.userprofile.name = display_name
    #                 old_user.userprofile.save()

    # def get_social_account(self, user, uid):
    #     app = SocialApp.objects.get_current('azure')
    #     social_account = SocialAccount(user=user, uid=uid, provider='azure', extra_data={'displayName': user.userprofile.name})
    #     social_account.app = app
    #     return social_account

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
