from django.conf.urls import url
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import AzureProvider

urlpatterns = default_urlpatterns(AzureProvider)
