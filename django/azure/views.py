from __future__ import unicode_literals

import requests
from django.conf import settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

from .provider import AzureProvider


LOGIN_URL = f'https://login.microsoftonline.com/{getattr(settings, "SOCIALACCOUNT_AZURE_TENANT", "common")}/oauth2/v2.0'
GRAPH_URL = 'https://graph.microsoft.com/v1.0'


# def get_users_from_azure():
#     token_url = f'https://login.microsoftonline.com/{settings.SOCIALACCOUNT_AZURE_TENANT}/oauth2/v2.0/token'
#     client_id = settings.SOCIALACCOUNT_PROVIDERS['azure']['APP']['client_id']
#     client_secret = settings.SOCIALACCOUNT_PROVIDERS['azure']['APP']['secret']

#     payload = {
#         'grant_type': 'client_credentials',
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'scope': 'https://graph.microsoft.com/.default',
#     }

#     response = requests.post(token_url, data=payload)
#     access_token = response.json().get('access_token')

#     if access_token:
#         headers = {'Authorization': f'Bearer {access_token}'}
#         users_url = 'https://graph.microsoft.com/v1.0/users'
#         users_response = requests.get(users_url, headers=headers)
#         users = users_response.json().get('value', [])
#         return users

#     return None

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_users(request):
#     users = get_users_from_azure()
#     if users is not None:
#         return Response(users)
#     else:
#         return Response({"error": "Failed to fetch users from Azure"}, status=400)

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


oauth2_login = OAuth2LoginView.adapter_view(AzureOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(AzureOAuth2Adapter)
