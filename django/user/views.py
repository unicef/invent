from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.views import TokenAuthMixin
from .serializers import (
    UserProfileSerializer,
    OrganisationSerializer,
    UserProfileListSerializer,
)
from .models import UserProfile, Organisation
from .serializers import ProfileJWTSerializer


class UserProfileViewSet(
    TokenAuthMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileListViewSet(TokenAuthMixin, ListModelMixin, GenericViewSet):
    # Fetch user and organisation objects in a single query using select_related,
    # and fetch related country objects in a separate query using prefetch_related,
    # which optimizes the number of database queries and improves performance.
    queryset = (
        UserProfile.objects.select_related("user", "organisation")
        .prefetch_related("country")
        .only(
            "id",
            "modified",
            "account_type",
            "name",
            "user__email",
            "organisation",
            "job_title",
            "department",
            "country",
            "region",
        )
    )
    serializer_class = UserProfileListSerializer


class OrganisationViewSet(
    TokenAuthMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # This method is used to generate and return the JWT token
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email

        return token.access_token

    # This method is used to validate the token and structure the response data
    def validate(self, attrs):
        # We call the superclass's method to do the standard validation and token generation
        data = super().validate(attrs)
        user_profile = getattr(self.user, "userprofile", None)
        if user_profile:
            user_profile_id = user_profile.id
            account_type = user_profile.account_type
        else:
            user_profile_id = None
            account_type = None

        # Restructure the data to match the desired format.
        # Get the 'access' value from the data and add the custom claims to the response
        data = {
            "token": data.pop("access"),
            "user_profile_id": user_profile_id,
            "account_type": account_type,
            "is_superuser": self.user.is_superuser,
        }
        return data


# This view is used to handle the token obtain pair endpoint
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email

        return token

    def validate(self, attrs):
        # We call the superclass's method to do the standard validation and token generation
        data = super().validate(attrs)
        user_profile = getattr(self.user, "userprofile", None)
        if user_profile:
            user_profile_id = user_profile.id
            account_type = user_profile.account_type
        else:
            user_profile_id = None
            account_type = None

        # Restructure the data to match the desired format.
        # Get the 'access' value from the data and add the custom claims to the response
        data = {
            "token": data.pop("access"),
            "user_profile_id": user_profile_id,
            "account_type": account_type,
            "is_superuser": self.user.is_superuser,
        }
        return data


class PasswordTokenObtainPairView(TokenObtainPairView):
    serializer_class = PasswordTokenObtainPairSerializer
