from allauth.account.utils import setup_user_email
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import DefaultAccountAdapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.response import Response
from rest_framework import status


from .models import UserProfile
from azure_services.views import AzureOAuth2Adapter
from django.contrib.auth import get_user_model
from django.conf import settings
from .views import CustomTokenObtainPairSerializer

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery  # noqa


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    def validate_unique_email(self, email):  # pragma: no cover
        return email


class AzureLogin(SocialLoginView):
    adapter_class = AzureOAuth2Adapter
    callback_url = settings.SOCIALACCOUNT_CALLBACK_URL
    client_class = OAuth2Client

    def get_response(self):
        # Your logic to build the response
        serializer = CustomTokenObtainPairSerializer()
        # Add validations here if needed
        custom_data = {
            "token": str(serializer.get_token(self.user)),
            "user": {
                "pk": self.user.pk,
                "username": self.user.username,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
                },
            "user_profile_id": self.user.userprofile.id if hasattr(self.user, 'userprofile') else None,
            "account_type": self.user.userprofile.account_type if hasattr(self.user, 'userprofile') else None,
            "is_superuser": self.user.is_superuser
        }
        return Response(custom_data, status=status.HTTP_200_OK)


class MyAzureAccountAdapter(DefaultSocialAccountAdapter):  # pragma: no cover
    def save_user(self, request, sociallogin, form=None):
        u = sociallogin.user
        u.set_unusable_password()
        DefaultAccountAdapterCustom().populate_username(request, u)
        assert not sociallogin.is_existing
        user = sociallogin.user
        name = sociallogin.account.extra_data.get("displayName")
        job_title = sociallogin.account.extra_data.get("jobTitle")
        department = sociallogin.account.extra_data.get("department")
        country = sociallogin.account.extra_data.get("country")

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
                country=country,
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
