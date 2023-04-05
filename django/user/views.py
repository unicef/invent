from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests

from core.views import TokenAuthMixin
from .serializers import UserProfileSerializer, OrganisationSerializer, UserProfileListSerializer
from .models import UserProfile, Organisation


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def azure_user_info(request):
    social_account = request.user.socialaccount_set.filter(provider='azure').first()

    if not social_account:
        return JsonResponse({"error": "Azure social account not found."}, status=404)

    access_token = social_account.socialtoken_set.first().token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    graph_url = 'https://graph.microsoft.com/v1.0/me'
    response = requests.get(graph_url, headers=headers)

    if response.status_code == 200:
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)


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
