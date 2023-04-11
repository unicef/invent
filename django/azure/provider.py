from __future__ import unicode_literals
import requests
import json
import os
import msal

from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

from django.contrib.auth import get_user_model


class AzureAccount(ProviderAccount):

    # TODO:
    # - avatar_url:
    #   https://developer.microsoft.com/en-us/graph/docs/api-reference/beta/api/profilephoto_get  # noqa
    def get_username(self):
        return self.account.extra_data['email']

    def to_str(self):
        name = '{0} {1}'.format(self.account.extra_data.get('first_name', ''),
                                self.account.extra_data.get('last_name', ''))
        if name.strip() != '':
            return name
        return super(AzureAccount, self).to_str()


class AzureProvider(OAuth2Provider):
    id = str('azure')
    name = 'Azure'
    account_class = AzureAccount

    def get_default_scope(self):
        """
        Doc on scopes available at
        https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-v2-scopes  # noqa
        """
        return ['User.Read', 'openid']

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        # Print the entire data object
        print("User data from Azure AD: ", data)

        new_users()

        email = data.get('mail')
        return dict(email=email,
                    username=email,
                    last_name=data.get('displayName'),
                    first_name=data.get('givenName'),
                    )


provider_classes = [AzureProvider]

def get_azure_ad_users():
    # Set up Microsoft Graph API authentication
    config = {
        "authority": "https://login.microsoftonline.com/" + os.environ.get('AZURE_TENANT', default=''),
        "client_id": os.environ.get('AZURE_CLIENT_ID', default=''),
        "client_secret": os.environ.get('AZURE_SECRET', default=''),
        "scope": ["https://graph.microsoft.com/.default"]
    }
    app = msal.ConfidentialClientApplication(
        config["client_id"], authority=config["authority"],
        client_credential=config["client_secret"]
    )
    result = app.acquire_token_silent(config["scope"], account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=config["scope"])
    if "access_token" in result:
        headers = {
            "Authorization": f"Bearer {result['access_token']}",
            "Content-Type": "application/json"
        }

        # Retrieve a list of users from Azure AD using the Microsoft Graph API
        response = requests.get(
            "https://graph.microsoft.com/v1.0/users",
            headers=headers,
        )
        return json.loads(response.text)
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))
        raise ValueError("Could not authenticate with Microsoft Graph API")



def new_users():
    # Call the get_azure_ad_users function and create new users in the Django app's database
    azure_ad_users = get_azure_ad_users()
    user_model = get_user_model()
    print("azure_ad_users:", azure_ad_users)
    print('user_model:', user_model)
    # for azure_ad_user in azure_ad_users["value"]:
    #     try:
    #         user_model.objects.get(username=azure_ad_user["userPrincipalName"])
    #     except user_model.DoesNotExist:
    #         user = user_model.objects.create_user(
    #             username=azure_ad_user["userPrincipalName"],
    #             email=azure_ad_user["mail"],
    #             first_name=azure_ad_user["givenName"],
    #             last_name=azure_ad_user["surname"],
    #         )
    #         print("the user: ", user)
    #         print("this is a new user: ", azure_ad_user)

    #         # user.save()
    #     break