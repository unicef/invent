import json
from pathlib import Path  # Remove after we receive actual AAD data
import requests

from allauth.account.utils import setup_user_email
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import DefaultAccountAdapter
from rest_auth.registration.views import SocialLoginView

from .models import UserProfile
from azure.views import AzureOAuth2Adapter
from country.models import Country
from django.contrib.auth import get_user_model
from django.conf import settings

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
        updated_users = []

        # Loop through the AAD users
        for azure_user in azure_users:
            email = azure_user['mail']
            display_name = azure_user['displayName']
            job_title = azure_user['jobTitle']
            department = azure_user['department']
            country_name = azure_user['country']
            social_account_uid = azure_user['id']

            # Try to get the User instance by email, if not found, create a new User instance
            try:
                user = user_model.objects.get(email=email)
            except user_model.DoesNotExist:
                user = user_model.objects.create(email=email, username=email)
                user.set_unusable_password()
                user.save()

            # Check if the user already exists in the local database
            try:
                old_user = user_model.objects.filter(email=user.email).get()
            except user_model.DoesNotExist:
                # If the user doesn't exist, create a new UserProfile instance

                # Get or create the Country instance for the user
                country, _ = Country.objects.get_or_create(name=country_name)

                # Create a new UserProfile instance for the user
                user_profile = UserProfile.objects.create(
                    user=user,
                    name=display_name,
                    account_type=UserProfile.DONOR,
                    job_title=job_title,
                    department=department,
                    country=country
                )
                # Add the created UserProfile instance to the updated_users list
                updated_users.append(user_profile)

            else:
                # If the user exists, update the existing UserProfile instance

                # Get or create the UserProfile instance for the user
                user_profile, created = UserProfile.objects.get_or_create(user=old_user)

                # Update the UserProfile instance with the new data
                user_profile.name = display_name
                user_profile.job_title = job_title
                user_profile.department = department

                # Get or create the Country instance for the user
                country, _ = Country.objects.get_or_create(name=country_name)
                user_profile.country = country

                # Save the updated UserProfile instance
                user_profile.save()
                # Add the updated UserProfile instance to the updated_users list
                updated_users.append(user_profile)

        # Return the list of updated UserProfile instances
        return updated_users

    def get_mocked_aad_users(self):
        # Get the path to the JSON file in the same directory as the adapters file
        json_file_path = Path(__file__).resolve().parent / 'mock_aad_users.json'

        # Read the JSON file
        with open(json_file_path, 'r') as file:
            users = json.load(file)

        return users

    def get_aad_users(self):
        url = 'https://graph.microsoft.com/v1.0/users'
        token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        users = []

        while url:
            response = requests.get(url, headers=headers)
            response_data = response.json()
            users.extend(response_data.get('value', []))

            # Print response details
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response text: {response.text}")

            url = response_data.get('@odata.nextLink', None)

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
