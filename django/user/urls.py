from django.conf import settings
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from allauth.account.views import confirm_email

from . import views as views

router = DefaultRouter()
router.register(r'userprofiles', views.UserProfileViewSet)
router.register(r'userprofiles', views.UserProfileListViewSet)
router.register(r'organisations', views.OrganisationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("django.contrib.auth.urls")),
    path('rest-auth/azure/', views.CustomTokenObtainPairView.as_view(), name='az_login'),
    path('api-token-auth/', views.CustomTokenObtainPairView.as_view(), name='api_token_auth'),
    re_path(r"^email-confirmation/(?P<key>\w+)/$", confirm_email, name="account_confirm_email"),
]

if settings.ENABLE_API_REGISTRATION:
    urlpatterns += [
        path("all-auth/", include("allauth.urls")),
        path("rest-auth/", include('dj_rest_auth.urls')),
        path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    ]
