from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from allauth.account.views import confirm_email
from rest_framework_jwt.views import obtain_jwt_token

from . import views as views
from .adapters import AzureLogin

router = DefaultRouter()
router.register(r'userprofiles', views.UserProfileViewSet)
router.register(r'userprofiles', views.UserProfileListViewSet)
router.register(r'organisations', views.OrganisationViewSet)

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^", include("django.contrib.auth.urls")),
    url(r"^all-auth/", include("allauth.urls")),
    url(r"^rest-auth/", include("rest_auth.urls")),
    url(r'^rest-auth/azure/', AzureLogin.as_view(), name='az_login'),
    url(r"^rest-auth/registration/DEPRECATED/", include("rest_auth.registration.urls")),
    url(r'^api-token-auth/', obtain_jwt_token, name="api_token_auth"),
    url(r"^email-confirmation/(?P<key>\w+)/$", confirm_email, name="account_confirm_email"),
]
