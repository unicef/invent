from django.conf.urls import url
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .views import UpdateAADUsersView, GetAADUsers
from .provider import AzureProvider

urlpatterns = default_urlpatterns(AzureProvider)

urlpatterns += [
    url(r"^get-aad-users/", GetAADUsers.as_view(), name="get_aad_users"),
    url(r"^update-aad-users/", UpdateAADUsersView.as_view(), name="update_aad_users"),
]
