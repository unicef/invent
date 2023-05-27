import logging
import requests
from time import sleep

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.conf import settings
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
            except requests.exceptions.RequestException as e:
                logger.error(f"Error while making request to {url}: {e}")
                retry_count += 1
                # TODO: Refactor. We need to have a fallback measurement in case Azure blocks the request
                sleep(2 * (2 ** retry_count))
        logger.info(
            f'Finished processing users. Total users processed: {processed_user_count}')

    def save_aad_users(self, users_batch):
        """
        Processes a batch of users fetched from AAD.
        The users in the batch are either created (if they do not exist) or updated (if they exist)
        in the local database.
        """
        new_users = []
        updated_users = []
        skipped_users = 0

        # Fetch all UserProfiles and map them to a dictionary with user id as the key
        user_profiles = UserProfile.objects.all().select_related('user')
        user_profiles_dict = {up.user.id: up for up in user_profiles}

        for user_data in users_batch:
            # Skip users with invalid email format
            if '@unicef.org' not in user_data['mail'].lower():
                skipped_users += 1
                continue

            username = user_data['mail'].split('@')[0]

            # Determine if user exists
            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    email=user_data['mail'],
                    defaults={'username': username},
                )

                # If user is new, create SocialAccount and UserProfile
                if created:
                    social_account = SocialAccount(
                        user=user, uid=user_data['id'])
                    user_profile = UserProfile(
                        user=user,
                        name=user_data.get('displayName', ''),
                        job_title=user_data.get('jobTitle', ''),
                        department=user_data.get('department', ''),
                        account_type=UserProfile.DONOR,
                    )
                    social_account.save()
                    user_profile.save()
                    new_users.append(user)
                else:
                    # Check and update UserProfile info if necessary from the dictionary
                    user_profile = user_profiles_dict.get(user.id)
                    if user_profile:
                        if not user_profile.name:
                            user_profile.name = user_data.get('displayName')
                        if not user_profile.job_title:
                            user_profile.job_title = user_data.get('jobTitle')
                        if not user_profile.department:
                            user_profile.department = user_data.get(
                                'department')
                        if user_profile.country is None and user_data.get('country') is not None:
                            try:
                                user_profile.country = Country.objects.get(
                                    name=user_data.get('country'))
                            except Country.DoesNotExist:
                                pass  # No matching country found, do nothing
                        updated_users.append(user_profile)

        # Bulk update UserProfile objects outside the loop after all updates have been made
        UserProfile.objects.bulk_update(
            updated_users, ['name', 'job_title', 'department', 'country'])

        logger.info(
            f'Batch processing completed. New users: {len(new_users)}, Updated users: {len(updated_users)}, Skipped users: {skipped_users}')

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
