from allauth.account.utils import setup_user_email
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import DefaultAccountAdapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.response import Response

from .models import UserProfile
from .views import CustomTokenObtainPairSerializer
from azure_services.views import AzureOAuth2Adapter
from django.contrib.auth import get_user_model
from django.conf import settings

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery  # noqa


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    def validate_unique_email(self, email):  # pragma: no cover
        return email


class AzureLogin(SocialLoginView):
    adapter_class = AzureOAuth2Adapter
    callback_url = settings.SOCIALACCOUNT_CALLBACK_URL
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        # Let the original post method do its work first (authentication)
        response = super().post(request, *args, **kwargs)
        
        # If the user is successfully authenticated, the response will be 200 OK
        if response.status_code == status.HTTP_200_OK:
            user = self.user  # Assuming `self.user` is set after the authentication
            
            # Create a token using your custom logic
            custom_token_serializer = CustomTokenObtainPairSerializer(data={})
            custom_token_serializer.user = user
            custom_token_serializer.is_valid(raise_exception=True)
            token = custom_token_serializer.get_token(user)
            
            # Modify the response data
            custom_data = {
                "token": str(token),
                "user": {
                    "pk": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "user_profile_id": getattr(user, 'userprofile', {}).get('id', None),
                "account_type": getattr(user, 'userprofile', {}).get('account_type', None),
                "is_superuser": user.is_superuser
            }
            print(f'custom_data: {custom_data}')
            response.data = custom_data
        
        return response


class MyAzureAccountAdapter(DefaultSocialAccountAdapter):  # pragma: no cover
    def save_user(self, request, sociallogin, form=None):
        u = sociallogin.user
        u.set_unusable_password()
        DefaultAccountAdapterCustom().populate_username(request, u)
        assert not sociallogin.is_existing
        user = sociallogin.user
        name = sociallogin.account.extra_data.get('displayName')
        job_title = sociallogin.account.extra_data.get('jobTitle')
        department = sociallogin.account.extra_data.get('department')
        country = sociallogin.account.extra_data.get('country')

        user_model = get_user_model()
        try:
            old_user = user_model.objects.filter(email=user.email).get()
        except user_model.DoesNotExist:
            user.save()
            sociallogin.account.user = user
            sociallogin.account.save()
            UserProfile.objects.create(
                user=user,
                name=name,
                account_type=UserProfile.DONOR,
                job_title=job_title,
                department=department,
                country=country
            )
            setup_user_email(request, user, sociallogin.email_addresses)
        else:
            sociallogin.account.user = old_user
            sociallogin.account.save()
            sociallogin.user = old_user
            if not old_user.userprofile.name:
                old_user.userprofile.name = name
                old_user.userprofile.job_title = job_title
                old_user.userprofile.department = department
                old_user.userprofile.save()

        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
