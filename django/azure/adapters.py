import logging
import requests
from time import sleep

from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

from country.models import Country
from user.models import UserProfile

# Initialize the logger at the module level
logger = logging.getLogger(__name__)


class AzureUserManagement:
    def process_aad_users(self, max_users=100):
        """
        Fetches and processes Azure Active Directory (AAD) users.

        This function fetches users from AAD in batches, processes them, and then
        fetches the next batch, repeating this process until either there are no
        more users to fetch or a maximum number of users have been processed.

        Parameters
            max_users (int, optional): The maximum number of users to process. Defaults to 100.

        Raises
            requests.exceptions.RequestException: If an error occurs while making the request to fetch users.
        """
        # Set initial url for fetching users
        url = settings.AZURE_GET_USERS_URL
        # Get access token and set headers for the request
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        retry_count = 0
        page_count = 0
        processed_user_count = 0
        # Fetch and process users in batches until either there are no more users to fetch
        # or the maximum number of users to process has been reached
        while url and retry_count < 5 and (max_users is None or processed_user_count < max_users):
            try:
                # Make request to fetch users
                response = requests.get(url, headers=headers)
                # Raise exception if status code is not 200
                response.raise_for_status()
                # Parse response data
                response_data = response.json()
                # Extract users from response data
                users_batch = response_data.get('value', [])
                logger.info(
                    f'Fetched {len(users_batch)} users in page {page_count+1}')
                processed_user_count += len(users_batch)

                # Process the batch of users right after fetching
                self.save_aad_users(users_batch)

                url = response_data.get('@odata.nextLink', None)
                page_count += 1
                retry_count = 0
                # TODO: Remove until further notice. If we stumple upon denial errors we can reinstate.
                # sleep(10)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error while making request to {url}: {e}")
                retry_count += 1
                # TODO: Refactor. We need to have a fallback measurement in case Azure blocks the request
                sleep(2 * (2 ** retry_count))
        logger.info(
            f'Finished processing users. Total users processed: {processed_user_count}')

    def save_aad_users(self, azure_users):
        logger.info(f"Total Azure users to be processed: {len(azure_users)}")

        user_model = get_user_model()
        batch_size = 100
        updated_users = []
        total_new_users = 0

        for i in range(0, len(azure_users), batch_size):
            batch = azure_users[i:i + batch_size]
            logger.info(f"Processing batch starting at index: {i}")

            existing_users_data, new_users_data = self.separate_users(batch)
            new_users = self.create_new_users(new_users_data, user_model)
            total_new_users += len(new_users)
            updated_users.extend(self.update_existing_users(
                existing_users_data, user_model))

        logger.info(
            f"Total existing users updated: {len(updated_users)}. Total new users created: {total_new_users}")
        return updated_users

    def separate_users(self, batch):
        batch_social_account_uids = [user.get('id') or '' for user in batch]
        existing_social_account_uids = set(SocialAccount.objects.filter(
            uid__in=batch_social_account_uids).values_list('uid', flat=True))

        new_users_data = []
        existing_users_data = []

        for azure_user in batch:
            user_data = self.get_user_data(azure_user)
            if user_data is None:
                continue  # Skip if user_data is None

            if user_data['social_account_uid'] in existing_social_account_uids:
                existing_users_data.append(user_data)
            else:
                new_users_data.append(user_data)

        return existing_users_data, new_users_data

    def get_user_data(self, azure_user):
        # Reject if email ends with "@unicef.org"
        email = azure_user.get('mail') or azure_user.get(
            'userPrincipalName') or ''
        if email.lower().endswith("@unicef.org"):
            return None
        # Otherwise, return the user data
        return {
            'email': email,
            'username': azure_user.get('mail') or azure_user.get('displayName') or azure_user.get('givenName') or azure_user.get('userPrincipalName') or '',
            'name': azure_user.get('displayName', ''),
            'job_title': azure_user.get('jobTitle', ''),
            'department': azure_user.get('department', ''),
            'country_name': azure_user.get('country', ''),
            'social_account_uid': azure_user.get('id', ''),
        }

    def create_new_users(self, new_users_data, user_model):
        new_users = []
        user_profiles = []
        social_accounts = []

        for user_data in new_users_data:
            # Skip if user data is None (e.g. due to email not being "@unicef.org")
            if user_data is None:
                continue
            user = user_model(
                email=user_data['email'], username=user_data['username'])
            user.set_unusable_password()
            new_users.append(user)

        try:  # catch the error here
            new_users = user_model.objects.bulk_create(new_users)
        except Exception as e:
            logger.error(f"Error while bulk creating users: {e}")
            logger.error(
                f"Batch of users that caused the error: {new_users_data}")
            return []

        for user, user_data in zip(new_users, new_users_data):
            user_profiles.append(self.get_user_profile(user, user_data))
            social_accounts.append(self.get_social_account(user, user_data))

        try:
            with transaction.atomic():
                UserProfile.objects.bulk_create(user_profiles, batch_size=100)
                SocialAccount.objects.bulk_create(
                    social_accounts, batch_size=100)
        except Exception as e:
            logger.error(
                f'Error while creating UserProfile and SocialAccount instances: {e}')

        return new_users

    def get_user_profile(self, user, user_data):
        try:
            country = Country.objects.get_or_create(name=user_data['country_name'])[
                0] if user_data['country_name'] else None
        except Exception:
            country = None

        return UserProfile(
            user=user,
            name=user_data['name'],
            job_title=user_data['job_title'],
            department=user_data['department'],
            country=country,
            account_type=UserProfile.DONOR,
        )

    def get_social_account(self, user, user_data):
        return SocialAccount(
            user=user, provider='azure', uid=user_data['social_account_uid'])

    def update_existing_users(self, existing_users_data, user_model):
        to_be_updated = []
        existing_users = user_model.objects.filter(
            email__in=[user_data['email'] for user_data in existing_users_data])
        existing_user_profiles = UserProfile.objects.filter(
            user__in=existing_users)

        for user_data, user_profile in zip(existing_users_data, existing_user_profiles):
            to_be_updated.append(
                self.update_user_profile(user_data, user_profile))

        try:
            with transaction.atomic():
                for profile in to_be_updated:
                    profile.save()
        except Exception as e:
            logger.error(f'Error while updating users: {e}')

        return to_be_updated

    def update_user_profile(self, user_data, user_profile):
        try:
            country = Country.objects.get(
                name=user_data['country_name']) if user_data['country_name'] else None
        except Country.DoesNotExist:
            country = None

        # If the user_profile's country field is None and a country was found, assign it
        if user_profile.country is None and country is not None:
            user_profile.country = country

        # If the user_profile's name field is None or empty, update it
        if not user_profile.name:
            user_profile.name = user_data['name']

        # Similarly, only update job_title and department if they are not already set
        if not user_profile.job_title:
            user_profile.job_title = user_data.get('job_title', '')

        if not user_profile.department:
            user_profile.department = user_data.get('department', '')

        return user_profile

    def get_aad_users(self, max_users=100):
        """
        Retrieves Azure Active Directory (AAD) users using Microsoft's Graph API.

        This function sends GET requests to the Graph API endpoint for users, handling pagination 
        by following the '@odata.nextLink' URL included in the response until no such link is present.
        If the request fails, it retries up to 5 times with exponential backoff to handle temporary issues.

        The function requires an access token which is fetched using the `get_access_token` method. 
        The users are returned as a list of dictionaries in the format provided by the Graph API. 
        The number of users fetched is limited by the 'max_users' parameter.

        Parameters:
            max_users (int, optional): The maximum number of users to fetch. Default is 100.

        Returns:
            list: A list of dictionaries where each dictionary represents an AAD user.

        Raises:
            requests.exceptions.RequestException: If a request to the Graph API fails.
        """
        max_users = int(max_users)
        url = settings.AZURE_GET_USERS_URL
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        users = []
        retry_count = 0
        page_count = 0
        while url and retry_count < 5 and len(users) < max_users:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                users_batch = response_data.get('value', [])
                users.extend(users_batch)
                logger.info(
                    f'Fetched {len(users_batch)} users in page {page_count+1}')
                logger.info(f'Users batch: {users_batch}')
                if len(users) > max_users:
                    # Limit the list to 'max_users' elements
                    users = users[:max_users]
                url = response_data.get('@odata.nextLink', None)
                page_count += 1
                retry_count = 0
                sleep(10)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error while making request to {url}: {e}")
                retry_count += 1
                sleep(10 * (2 ** retry_count))
        logger.info(
            f'Finished fetching users. Total users fetched: {len(users)}')
        return users

    def get_access_token(self):
        """
        This method is used to retrieve an access token from Azure AD.

        The access token is needed to authenticate and authorize requests made to Azure AD Graph API.
        This method sends a POST request to the Azure AD OAuth2 token endpoint with necessary details like client ID,
        client secret, and resource URL.

        The access token is returned from the function if the request is successful. If the request fails,
        it logs the error and returns None.

        Returns:
            str: The access token if the request is successful. None otherwise.
        """
        # Azure AD tenant ID
        tenant_id = settings.SOCIALACCOUNT_AZURE_TENANT
        # Azure AD client ID
        client_id = settings.SOCIALACCOUNT_PROVIDERS['azure']['APP']['client_id']
        # Azure AD client secret
        client_secret = settings.SOCIALACCOUNT_PROVIDERS['azure']['APP']['secret']
        # Resource URL for which the token is needed
        resource = 'https://graph.microsoft.com'
        # Azure AD OAuth2 token endpoint URL
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'

        # Payload for the POST request
        payload = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': resource
        }

        # Send a POST request to the Azure AD OAuth2 token endpoint
        response = requests.post(url, data=payload)

        # If the request is successful
        if response.status_code == 200:
            # Parse the JSON response
            json_response = response.json()
            # Extract the access token from the response
            access_token = json_response['access_token']
            # Return the access token
            return access_token
        else:
            # Log the error if the request fails
            logger.error(
                f"Failed to get access token. Status code: {response.status_code}, Response: {response.text}")
            # Return None if the request fails
            return None

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
