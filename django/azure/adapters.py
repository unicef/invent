import logging
import requests
from time import sleep

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.conf import settings
from django.db import transaction, DatabaseError


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

        total_new_users = 0
        total_updated_users = []
        total_skipped_users = 0
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
                new_users, updated_users, skipped_users = self.save_aad_users(
                    users_batch)

                # Update totals
                total_new_users += len(new_users)
                # We extend the list now
                total_updated_users.extend(updated_users)
                total_skipped_users += len(skipped_users)

                url = response_data.get('@odata.nextLink', None)
                page_count += 1
                retry_count = 0
            except requests.exceptions.RequestException as e:
                logger.error(f"Error while making request to {url}: {e}")
                retry_count += 1
                # TODO: Refactor. We need to have a fallback measurement in case Azure blocks the request
                sleep(2 * (2 ** retry_count))

        logger.info(
            f'Finished processing users. Total users processed: {processed_user_count}. '
            f'Total new users created: {total_new_users}. '
            f'Total current users updated: {len(total_updated_users)}. '
            f'Total users skipped due to inconsistencies: {total_skipped_users}.\n'
            f'Updated users details: '
            f'{[(user["user"].id, user["user"].email, user["changes"]) for user in total_updated_users]}'
        )

    def save_aad_users(self, users_batch):
        """
        Process a batch of users fetched from AAD.

        For each user in the batch, the function checks if the user exists in the local database.
        If the user doesn't exist, it creates a new User and UserProfile instance.
        If the user does exist, it updates the user's information based on the new data fetched from AAD.

        Parameters
        ----------
        users_batch : list
            A list of dictionaries where each dictionary contains data for a user fetched from AAD.

        Returns
        -------
        None
        """
        # Track the new and updated users
        new_users = []
        updated_users = []
        skipped_users = []

        # Fetch all User objects in this batch
        user_emails_in_batch = [user_data['mail'].lower(
        ) for user_data in users_batch if user_data.get('mail')]
        existing_users = User.objects.filter(email__in=user_emails_in_batch)
        existing_users_dict = {user.email: user for user in existing_users}
        # for faster "in" checks
        existing_users_set = set(existing_users_dict.keys())

        # Fetch all UserProfile objects in this batch and map them to their respective User's id for easy access
        user_profiles = UserProfile.objects.filter(
            user__email__in=user_emails_in_batch).select_related('user')
        user_profiles_dict = {up.user.email: up for up in user_profiles}

        # Process each user data in the batch
        for user_data in users_batch:
            try:
                # Skip the user if 'mail' field is not in user_data, if the mail is None, or if the mail does not end with '@unicef.org'
                if not user_data.get('mail') or '@unicef.org' not in user_data['mail'].lower():
                    skipped_users.append(user_data)
                    continue

                # Ensure database consistency even if an error occurs while processing a user
                with transaction.atomic():
                    # Get the email in lowercase and the username in a case-insensitive manner
                    email = user_data['mail'].lower()
                    username = email.split('@')[0] if '@' in email else ''

                    # Get the first name and last name from the user data
                    first_name = user_data.get('givenName', '') or ''
                    last_name = user_data.get('surname', '') or ''

                    # Instantiate changes dictionary here for each user
                    changes = {}

                    # Check if the user already exists in the existing_users_set
                    if email not in existing_users_set:
                        # Create a new user
                        user = User.objects.create(
                            email=email, username=username,
                            first_name=first_name, last_name=last_name)

                        try:
                            # Create and save a new SocialAccount and UserProfile for the new user
                            social_account = SocialAccount(
                                user=user, uid=user_data['id'])
                            user_profile = UserProfile(user=user, name=user_data.get('displayName', ''),
                                                       job_title=user_data.get('jobTitle', ''), department=user_data.get('department', ''),
                                                       account_type=UserProfile.DONOR)
                            social_account.save()
                            user_profile.save()
                            # Keep track of the new user
                            new_users.append(user)
                        except Exception as e:
                            logger.error(
                                f'Error while creating SocialAccount or UserProfile for new user {user.email}: {e}')
                    else:
                        # If the user was not created i.e. the user already exists
                        # Get the user's profile
                        user = existing_users_dict.get(email)
                        user_profile = user_profiles_dict.get(user.email)
                        if user_profile:
                            is_profile_updated = False
                            # Check if the user's first name or last name has changed
                            if user.first_name != first_name:
                                old_first_name = user.first_name
                                user.first_name = first_name
                                is_profile_updated = True
                                changes['first_name'] = {
                                    'previous': old_first_name, 'updated': first_name}
                            if user.last_name != last_name:
                                old_last_name = user.last_name
                                user.last_name = last_name
                                is_profile_updated = True
                                changes['last_name'] = {
                                    'previous': old_last_name, 'updated': last_name}

                            # Update the user profile's fields if they have changed
                            for field in ['name', 'job_title', 'department']:
                                new_value = user_data.get(field)
                                current_value = getattr(user_profile, field)
                                if new_value is not None and current_value != new_value:
                                    setattr(user_profile, field, new_value)
                                    is_profile_updated = True
                                    changes[field] = {
                                        'previous': current_value, 'updated': new_value}
                                elif new_value is None and current_value is not None:
                                    # If the new value is None but the current value is not None, ignore the update
                                    pass
                                elif new_value is None and current_value is None:
                                    # If both the new value and the current value are None, also ignore the update
                                    pass
                                elif new_value == current_value:
                                    # If the new value is the same as the current value, also ignore the update
                                    pass
                                else:
                                    # In all other cases, don't consider this as an update
                                    pass

                            # Update the user's country if it is not set
                            if user_profile.country is None and user_data.get('country') is not None:
                                try:
                                    country = Country.objects.get(
                                        name=user_data.get('country'))
                                    user_profile.country = country
                                    is_profile_updated = True
                                except Country.DoesNotExist:
                                    # If the country doesn't exist in the database, don't count this as an update
                                    pass
                            elif user_profile.country is None and user_data.get('country') is None:
                                # If the country value from AAD is also None, don't count this as an update
                                pass
                            else:
                                # If the user_profile.country is not None, we may have other fields to update
                                pass
                            # If the user profile or the user was updated, save it and keep track of the updated user
                            if is_profile_updated and changes:
                                user.save()
                                user_profile.save()
                                # Append user with changes to the updated_users list
                                if changes:
                                    updated_users.append(
                                        {'user': user_profile.user, 'changes': changes})
            except DatabaseError as e:
                logger.error(
                    f'Database error while processing user {user_data}: {e}')
            except KeyError as e:
                logger.error(f'Missing key in user data {user_data}: {e}')
            except Exception as e:
                logger.error(
                    f'Other error while processing user {user_data}: {e}')
        logger.info(
            f'New users created: {len(new_users)}. Current users updated: {len(updated_users)}. Skipped users: {len(skipped_users)}.')

        return new_users, updated_users, skipped_users

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
