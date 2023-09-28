from django.urls import path
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .views import UpdateAADUsersView
from .provider import AzureProvider

urlpatterns = default_urlpatterns(AzureProvider)

urlpatterns += [
    path("update-aad-users/", UpdateAADUsersView.as_view(), name="update_aad_users"),
]
