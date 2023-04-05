from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from core.views import TokenAuthMixin
from .serializers import UserProfileSerializer, OrganisationSerializer, UserProfileListSerializer
from .models import UserProfile, Organisation

# Add this function to views.py


def get_azure_user_info(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required."}, status=401)

    social_account = request.user.socialaccount_set.filter(provider='azure').first()
    if not social_account:
        return JsonResponse({"error": "Social account not found."}, status=404)

    extra_data = social_account.extra_data

    user_info = {
        "email": extra_data.get("mail"),
        "first_name": extra_data.get("givenName"),
        "last_name": extra_data.get("surname"),
        "display_name": extra_data.get("displayName"),
    }

    return JsonResponse(user_info)


class UserProfileViewSet(TokenAuthMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileListViewSet(TokenAuthMixin, ListModelMixin, GenericViewSet):
    queryset = UserProfile.objects.select_related('user', 'organisation').only('id', 'modified', 'account_type',
                                                                               'name', 'user__email', 'organisation')
    serializer_class = UserProfileListSerializer


class OrganisationViewSet(TokenAuthMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        """
        Retrieves Organisation objects, filtered by search term if present,
        for autocomplete of organisation fields.
        """
        search_term = self.request.query_params.get("name")
        if search_term:
            return Organisation.objects.filter(name__contains=search_term)
        else:
            return Organisation.objects.all()
