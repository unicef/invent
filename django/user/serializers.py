from rest_framework import serializers
from rest_auth.serializers import JWTSerializer
from rest_framework.exceptions import ValidationError

from country.models import Country
from project.models import Project, Portfolio, ReviewScore
from .models import UserProfile, Organisation


class ProfileJWTSerializer(JWTSerializer):
    """
    Retrieves the token and userprofile of a given user after log in.
    """
    token = serializers.CharField()
    user = serializers.SerializerMethodField()
    user_profile_id = serializers.SerializerMethodField()
    account_type = serializers.SerializerMethodField()
    is_superuser = serializers.SerializerMethodField()

    @staticmethod
    def get_user_profile_id(obj):  # pragma: no cover
        """
        Checks the UserProfile existence for the given key.
        """
        if hasattr(obj['user'], 'userprofile'):
            return obj['user'].userprofile.id

    @staticmethod
    def get_account_type(obj):  # pragma: no cover
        """
        Checks the UserProfile existence for the given key.
        """
        if hasattr(obj['user'], 'userprofile'):
            return obj['user'].userprofile.account_type

    @staticmethod
    def get_is_superuser(obj):
        return obj['user'].is_superuser


class UserProfileListSerializer(serializers.ModelSerializer):
    # Use source argument to map email field to user.email
    email = serializers.EmailField(source='user.email', read_only=True)
    # Use SerializerMethodField to fetch the country name instead of the country id
    country = serializers.SerializerMethodField(method_name='get_country_name')

    class Meta:
        model = UserProfile
        fields = ('id', 'modified', 'account_type', 'name', 'email',
                  'organisation', 'job_title', 'department', 'country', 'region')

    # Custom method to get the country name from the UserProfile instance
    def get_country_name(self, obj):
        if obj.country is not None:
            return obj.country.name
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    name = serializers.CharField(
        required=True, allow_blank=False, allow_null=False)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=True,
                                                 allow_null=False)
    organisation = serializers.PrimaryKeyRelatedField(queryset=Organisation.objects.all(), required=True,
                                                      allow_null=False)
    job_title = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    department = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    member = serializers.SerializerMethodField()
    viewer = serializers.SerializerMethodField()
    is_superuser = serializers.SerializerMethodField()
    account_type_approved = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField(required=False)
    global_portfolio_owner = serializers.NullBooleanField(required=False)
    favorite = serializers.SerializerMethodField(required=False)
    reviews = serializers.SerializerMethodField(required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    @staticmethod
    def get_member(obj):
        return Project.objects.owner_of(obj.user).values_list('id', flat=True)

    @staticmethod
    def get_viewer(obj):
        return Project.objects.viewer_of(obj.user).values_list('id', flat=True)

    @staticmethod
    def get_is_superuser(obj):
        if hasattr(obj, 'user'):
            return obj.user.is_superuser

    @staticmethod
    def get_manager(obj):
        if hasattr(obj, 'user'):
            return Portfolio.objects.is_manager(obj.user).values_list('id', flat=True)

    @staticmethod
    def get_reviews(obj):
        return ReviewScore.objects.filter(reviewer=obj).values_list('id', flat=True)

    @staticmethod
    def get_account_type_approved(obj):
        if obj.account_type == UserProfile.DONOR and obj.donor:
            return obj in obj.donor.users.all()
        elif obj.account_type == UserProfile.DONOR_ADMIN and obj.donor:
            return obj in obj.donor.admins.all()
        elif obj.account_type == UserProfile.SUPER_DONOR_ADMIN and obj.donor:
            return obj in obj.donor.super_admins.all()
        elif obj.account_type == UserProfile.GOVERNMENT and obj.country:
            return obj in obj.country.users.all()
        elif obj.account_type == UserProfile.COUNTRY_ADMIN and obj.country:
            return obj in obj.country.admins.all()
        elif obj.account_type == UserProfile.SUPER_COUNTRY_ADMIN and obj.country:
            return obj in obj.country.super_admins.all()
        return False

    @staticmethod
    def get_favorite(obj):
        return Project.objects.published_only().favorited_by(obj.user).values_list('id', flat=True)

    def validate(self, attrs):
        if attrs.get('account_type') in [UserProfile.DONOR, UserProfile.DONOR_ADMIN, UserProfile.SUPER_DONOR_ADMIN]:
            if not attrs.get('donor'):
                raise ValidationError({'donor': 'Donor is required'})
        return attrs


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'
