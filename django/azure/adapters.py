import logging
import requests
from time import sleep

from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

from country.models import Country
from user.models import UserProfile


class AzureUserManagement:
    def save_aad_users(self, azure_users):
        """
        This method updates the application's user database with information fetched from Azure AD.
        It processes the users in batches to increase efficiency and reduce potential for errors or timeouts.

        It separates out new users and existing users to handle them differently, creating new user entries for new users 
        and updating existing entries for existing users. It uses Django's `bulk_create` and `bulk_update` methods 
        to perform these operations more efficiently.

        The whole process for each batch is wrapped in a database transaction to ensure data integrity. 
        If any part of the process fails, the transaction will be rolled back to the state it was in before the transaction started.

        Parameters:
            azure_users (list): A list of dictionaries where each dictionary represents a user fetched from Azure AD. 
            Each dictionary contains user attributes like email, name, job title, department, country, etc.

        Returns:
        list: A list of UserProfile objects that were updated or created in the process.
        """
        logger = logging.getLogger(__name__)
        # Log the total number of users to be processed
        logger.info(f"Total Azure users to be processed: {len(azure_users)}")

        # Get the User model
        user_model = get_user_model()
        # Set the number of users to process in each batch
        batch_size = 100
        # Initialize a list to hold the users that have been updated
        updated_users = []

        # Process the users in batches
        for i in range(0, len(azure_users), batch_size):
            # Create a batch of users to process
            batch = azure_users[i:i + batch_size]

            logger.info(f"Processing batch starting at index: {i}")

            # Initialize lists to hold data for new and existing users
            new_users_data = []
            existing_users_data = []

            # Get a set of existing email addresses
            existing_emails = set(
                user_model.objects.values_list('email', flat=True))

            # Separate the users in the batch into new and existing users
            for azure_user in batch:
                # Create a dictionary to hold the user's data
                user_data = {
                    'email': azure_user['mail'],
                    'username': azure_user['mail'],
                    'name': azure_user['displayName'],
                    'job_title': azure_user.get('jobTitle', ''),
                    'department': azure_user.get('department', ''),
                    'country_name': azure_user['country'],
                    'social_account_uid': azure_user['id'],
                }
                # Check if the user's email is already in the database
                if user_data['email'] in existing_emails:
                    existing_users_data.append(user_data)
                else:
                    new_users_data.append(user_data)

            # Create new users and social accounts
            new_users = []
            user_profiles = []
            social_accounts = []

            # Create a new User, UserProfile, and SocialAccount for each new user
            for user_data in new_users_data:
                # Get or create the user's country
                country, _ = Country.objects.get_or_create(
                    name=user_data['country_name'])

                # Create a new User
                user = user_model(
                    email=user_data['email'], username=user_data['username'])
                user.set_unusable_password()

                # Create a new UserProfile
                user_profiles.append(UserProfile(
                    user=user,
                    name=user_data['name'],
                    job_title=user_data['job_title'],
                    department=user_data['department'],
                    country=country,
                    account_type=UserProfile.DONOR,
                    social_account_uid=user_data['social_account_uid']
                ))

                # Create a new SocialAccount
                social_accounts.append(SocialAccount(
                    user=user, provider='azure', uid=user_data['social_account_uid']))

                new_users.append(user)

            # Use a transaction to create the new users, user profiles, and social accounts
            try:
                with transaction.atomic():
                    user_model.objects.bulk_create(new_users, batch_size=100)
                    UserProfile.objects.bulk_create(
                        user_profiles, batch_size=100)
                    SocialAccount.objects.bulk_create(
                        social_accounts, batch_size=100)
            except Exception as e:
                # Log any errors that occur during the creation process
                logger.error(f'Error while creating users: {e}')

            # Initialize a list to hold the users that need to be updated
            to_be_updated = []
            for user_data in existing_users_data:
                user = user_model.objects.get(email=user_data['email'])
                country, _ = Country.objects.get_or_create(
                    name=user_data['country_name'])
                user_profile = UserProfile.objects.get(user=user)

                # Update the user's profile
                user_profile.name = user_data['name']
                user_profile.job_title = user_data.get('job_title', '')
                user_profile.department = user_data.get('department', '')
                user_profile.country = country
                user_profile.social_account_uid = user_data['social_account_uid']

                # Add the updated profile to the list of profiles to be updated
                to_be_updated.append(user_profile)

            # Use a transaction to update the user profiles
            try:
                with transaction.atomic():
                    # bulk_update is used to perform the updates in a single query for efficiency
                    UserProfile.objects.bulk_update(to_be_updated, [
                                                    'name', 'job_title', 'department', 'country', 'social_account_uid'], batch_size=100)
                    # Add the updated profiles to the list of all updated users
                    updated_users.extend(to_be_updated)
            except Exception as e:
                # Log any errors that occur during the update process
                logger.error(f'Error while updating users: {e}')

        # Log the total number of updated users
        logger.info(f"Total updated users: {len(updated_users)}")

        # Return the list of updated users
        return updated_users

    def get_aad_users(self):
        """
        Retrieves Azure Active Directory (AAD) users using Microsoft's Graph API.

        This function sends GET requests to the Graph API endpoint for users, handling pagination 
        by following the '@odata.nextLink' URL included in the response until no such link is present.
        If the request fails, it retries up to 5 times with exponential backoff to handle temporary issues.

        The function requires an access token which is fetched using the `get_access_token` method. 
        The users are returned as a list of dictionaries in the format provided by the Graph API.

        Returns:
            list: A list of dictionaries where each dictionary represents an AAD user.

        Raises:
            requests.exceptions.RequestException: If a request to the Graph API fails.
        """
        logger = logging.getLogger(__name__)
        # Define the endpoint URL.
        url = 'https://graph.microsoft.com/v1.0/users'

        # Get the access token.
        token = self.get_access_token()

        # Prepare the request headers.
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Initialize an empty list to hold the users.
        users = []

        # Initialize the retry count to 0.
        retry_count = 0

        # Keep sending requests as long as there's a next page URL and the retry limit hasn't been reached.
        while url and retry_count < 5:
            try:
                # Send the request.
                response = requests.get(url, headers=headers)
                # Raise an exception if the request was unsuccessful.
                response.raise_for_status()
                # Parse the response JSON.
                response_data = response.json()
                # Add the users from the current page to the list.
                users.extend(response_data.get('value', []))
                # Get the URL for the next page.
                url = response_data.get('@odata.nextLink', None)
                # Reset the retry count after a successful request.
                retry_count = 0
                # Wait for 10 seconds to avoid hitting the rate limit.
                sleep(10)
            except requests.exceptions.RequestException as e:
                # Log the error and increment the retry count.
                logger.error(f"Error while making request to {url}: {e}")
                retry_count += 1
                # Use exponential backoff when retrying.
                sleep(10 * (2 ** retry_count))

        # Return the list of users.
        return users

    def get_mock_aad_users(self, max_users=100):
        logger = logging.getLogger(__name__)
        max_users = int(max_users)
        base_url = 'https://graph.microsoft.com/v1.0/users'
        url = f'{base_url}?$top=100'
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
                logger.info(f'Response data: {response_data}')
                users_batch = response_data.get('value', [])
                users.extend(users_batch)
                logger.info(f'Fetched {len(users_batch)} users in page {page_count+1}')
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
        logger.info(f'Finished fetching users. Total users fetched: {len(users)}')
        return users


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

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
