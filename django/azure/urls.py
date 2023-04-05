from django.urls import path
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import AzureProvider
from . import views

urlpatterns = default_urlpatterns(AzureProvider)

urlpatterns += [
    path('users/', views.fetch_all_users, name='all_users'),
]
