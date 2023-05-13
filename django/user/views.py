from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.views import TokenAuthMixin
from .serializers import UserProfileSerializer, OrganisationSerializer, UserProfileListSerializer
from .models import UserProfile, Organisation
from .adapters import MyAzureAccountAdapter
from user.tasks import fetch_users_from_aad_and_update_db


class UserProfileViewSet(TokenAuthMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileListViewSet(TokenAuthMixin, ListModelMixin, GenericViewSet):
    # Fetch user and organisation objects in a single query using select_related,
    # and fetch related country objects in a separate query using prefetch_related,
    # which optimizes the number of database queries and improves performance.
    queryset = UserProfile.objects.select_related('user', 'organisation').prefetch_related('country').only(
        'id', 'modified', 'account_type', 'name', 'user__email', 'organisation', 'job_title', 'department', 'country')
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


class GetAADUsers(TokenAuthMixin, APIView):
    """
    API View to fetch Azure Active Directory (AAD) users.
    Requires token authentication.
    """

    def get(self, request, format=None):
        # Create an instance of MyAzureAccountAdapter and fetch the AAD users
        adapter = MyAzureAccountAdapter()
        azure_users = adapter.get_aad_users()

        # Return the AAD users in the response
        return Response({'users': azure_users}, status=status.HTTP_200_OK)



class UpdateAADUsersView(TokenAuthMixin, APIView):
    """
    API View to update and save Azure Active Directory (AAD) users in the local database.
    It fetches the AAD users, saves them, and returns the updated users' profiles.
    Requires token authentication.
    """

    def put(self, request, format=None):
        # Call the Celery task to fetch and update the users
        fetch_users_from_aad_and_update_db.delay()

        return Response({'message': 'Azure users update started.'}, status=status.HTTP_202_ACCEPTED)