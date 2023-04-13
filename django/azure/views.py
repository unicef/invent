from __future__ import unicode_literals

import json
import requests
from django.conf import settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import AzureProvider


LOGIN_URL = f'https://login.microsoftonline.com/{getattr(settings, "SOCIALACCOUNT_AZURE_TENANT", "common")}/oauth2/v2.0'
GRAPH_URL = 'https://graph.microsoft.com/v1.0'


class AzureOAuth2Adapter(OAuth2Adapter):
    """
    Docs available at:
    https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-v2-protocols
    """
    provider_id = AzureProvider.id
    access_token_url = LOGIN_URL + '/token'
    authorize_url = LOGIN_URL + '/authorize'
    profile_url = 'https://graph.microsoft.com/v1.0/me'
    # Can be used later to obtain group data. Needs 'Group.Read.All' or
    # similar.
    #
    # See https://developer.microsoft.com/en-us/graph/docs/api-reference/beta/api/user_list_memberof  # noqa
    groups_url = GRAPH_URL + '/me/memberOf?$select=displayName'

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        extra_data = {}

        resp = requests.get(self.profile_url, headers=headers)

# See:
#
# https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/user_get  # noqa
#
# example of what's returned (in python format)
#
# {u'displayName': u'John Smith', u'mobilePhone': None,
#  u'preferredLanguage': u'en-US', u'jobTitle': u'Director',
#  u'userPrincipalName': u'john@smith.com',
#  u'@odata.context':
#  u'https://graph.microsoft.com/v1.0/$metadata#users/$entity',
#  u'officeLocation': u'Paris', u'businessPhones': [],
#  u'mail': u'john@smith.com', u'surname': u'Smith',
#  u'givenName': u'John', u'id': u'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'}

        profile_data = resp.json()
        extra_data.update(profile_data)

        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)

    def get_aad_users(self):
        users = []

        mock_users_json = '''
            [
                {
                    "id": "1",
                    "displayName": "John Doe",
                    "givenName": "John",
                    "surname": "Doe",
                    "mail": "john.doe@example.com",
                    "jobTitle": "Software Engineer",
                    "userPrincipalName": "john.doe@example.com",
                    "mobilePhone": "+1 555 555 5555",
                    "officeLocation": "New York",
                    "preferredLanguage": "en-US",
                    "businessPhones": ["+1 555 555 5555"],
                    "memberOf": ["Group 1", "Group 2"],
                    "country": "United States",
                    "department": "Engineering"
                },
                {
                    "id": "2",
                    "displayName": "Jane Doe",
                    "givenName": "Jane",
                    "surname": "Doe",
                    "mail": "jane.doe@example.com",
                    "jobTitle": "Project Manager",
                    "userPrincipalName": "jane.doe@example.com",
                    "mobilePhone": "+1 555 555 5555",
                    "officeLocation": "San Francisco",
                    "preferredLanguage": "en-US",
                    "businessPhones": ["+1 555 555 5555"],
                    "memberOf": ["Group 1", "Group 3"],
                    "country": "United States",
                    "department": "Project Management"
                }
            ]
        '''

        users = json.loads(mock_users_json)

        return users
    

    # def get_aad_users(self):
    #     url = 'https://graph.microsoft.com/v1.0/users'
    #     token = self.get_access_token()

    #     headers = {
    #         'Authorization': f'Bearer {token}',
    #         'Content-Type': 'application/json'
    #     }

    #     users = []

    #     while url:
    #         response = requests.get(url, headers=headers)
    #         response_data = response.json()
    #         users.extend(response_data.get('value', []))

    #         url = response_data.get('@odata.nextLink', None)

    #     return users


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


oauth2_login = OAuth2LoginView.adapter_view(AzureOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(AzureOAuth2Adapter)
