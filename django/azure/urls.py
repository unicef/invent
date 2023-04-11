from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import AzureProvider
from django.azure.new_users import new_user

new_user()

urlpatterns = default_urlpatterns(AzureProvider)
