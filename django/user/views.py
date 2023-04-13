from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.views import TokenAuthMixin
from .serializers import UserProfileSerializer, OrganisationSerializer, UserProfileListSerializer
from .models import UserProfile, Organisation

from .adapters import MyAzureAccountAdapter, AzureOAuth2Adapter


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


class UpdateAADUsersView(APIView):
    def get(self, request, format=None):
        adapter = MyAzureAccountAdapter()
        azure_adapter = AzureOAuth2Adapter()

        azure_users = azure_adapter.get_aad_users()
        adapter.save_users_from_azure(azure_users)

        return Response({'message': 'Azure users saved successfully.'}, status=status.HTTP_200_OK)


class GetAADUsers(APIView):
    def get(self, request, format=None):
        azure_adapter = AzureOAuth2Adapter()
        azure_users = azure_adapter.get_aad_users()

        return Response({'users': azure_users}, status=status.HTTP_200_OK)
