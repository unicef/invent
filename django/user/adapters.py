import requests
from time import sleep

from allauth.account.utils import setup_user_email
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import DefaultAccountAdapter
from rest_auth.registration.views import SocialLoginView

from .models import UserProfile
from azure.views import AzureOAuth2Adapter
from country.models import Country
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Q

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
        batch_size = 1000  # number of users to process at once
        updated_users = []

        for i in range(0, len(azure_users), batch_size):
            batch = azure_users[i:i + batch_size]

            # Prepare data for new users and existing users
            new_users_data = []
            existing_users_data = []
            for azure_user in batch:
                user_data = {
                    'email': azure_user['mail'],
                    'username': azure_user['mail'],
                    'name': azure_user['displayName'],
                    'job_title': azure_user['jobTitle'],
                    'department': azure_user['department'],
                    'country_name': azure_user['country'],
                    'social_account_uid': azure_user['id'],
                }
                if user_model.objects.filter(email=user_data['email']).exists():
                    existing_users_data.append(user_data)
                else:
                    new_users_data.append(user_data)

            # Create new users and social accounts
            new_users = []
            user_profiles = []
            social_accounts = []
            for user_data in new_users_data:
                country, _ = Country.objects.get_or_create(
                    name=user_data['country_name'])
                user = user_model(
                    email=user_data['email'], username=user_data['username'])
                user.set_unusable_password()
                user_profiles.append(UserProfile(
                    user=user,
                    name=user_data['name'],
                    job_title=user_data['job_title'],
                    department=user_data['department'],
                    country=country,
                    account_type=UserProfile.DONOR,
                    social_account_uid=user_data['social_account_uid']
                ))
                social_accounts.append(SocialAccount(
                    user=user, provider='azure', uid=user_data['social_account_uid']))
                new_users.append(user)

            try:
                with transaction.atomic():
                    # Using bulk_create to create new users, user profiles, and social accounts
                    user_model.objects.bulk_create(new_users)
                    UserProfile.objects.bulk_create(user_profiles)
                    SocialAccount.objects.bulk_create(social_accounts)
            except Exception as e:
                # Log the error
                print(f'Error while creating users: {e}')

            try:
                # Update existing users
                for user_data in existing_users_data:
                    user = user_model.objects.get(email=user_data['email'])
                    country, _ = Country.objects.get_or_create(
                        name=user_data['country_name'])
                    user_profile = UserProfile.objects.get(user=user)
                    user_profile.name = user_data['name']
                    user_profile.job_title = user_data['job_title']
                    user_profile.department = user_data['department']
                    user_profile.country = country
                    user_profile.social_account_uid = user_data['social_account_uid']
                    user_profile.save()
                    updated_users.append(user_profile)
            except Exception as e:
                # Log the error
                print(f'Error while updating user {user.email}: {e}')

        return updated_users

    def get_aad_users(self):
        url = 'https://graph.microsoft.com/v1.0/users?$top=1000'
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        users = []

        while url:
            try:
                response = requests.get(url, headers=headers)
                response_data = response.json()
                users.extend(response_data.get('value', []))
                url = response_data.get('@odata.nextLink', None)

                # Throttle the API calls
                sleep(10)
            except Exception as e:
                print(f"Error while making request to {url}: {e}")
                break  # stop fetching users if there's an error
        return users

    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def get_access_token(self):
        tenant_id = settings.SOCIALACCOUNT_AZURE_TENANT
        client_id = settings.SOCIALACCOUNT_PROVIDERS['azure']['APP']['client_id']
        client_secret = settings.SOCIALACCOUNT_PROVIDERS['azure']['APP']['secret']
        resource = 'https://graph.microsoft.com'
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'

        payload = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': resource
        }

        response = requests.post(url, data=payload)
        if response.status_code == 200:
            json_response = response.json()
            access_token = json_response['access_token']
            return access_token
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
