from import_export import resources
from import_export.fields import Field
from django.utils.translation import ugettext_lazy as _

from user.models import UserProfile
from django.contrib.auth.models import User


class UserResource(resources.ModelResource):  # pragma: no cover
    """
    This class is basically a serializer for the django-import-export module
    Fields:
     - Stats:
       - last login
       - date joined
       - ODK Synced
     - Permissions:
       - Active
       - Staff Status
       - Superuser Status
       - Global portfolio owner
     - User Info
       - email address
       - name
       - account type
       - Organization
       - Country
       - Donor
       - Language
    """
    # Stats
    last_login = Field(column_name=_('Last login date'))
    date_joined = Field(column_name=_('Date joined'))
    is_odk_synced = Field(column_name=_('Synced to ODK?'))
    # Permissions
    is_active = Field(column_name=_('Active?'))
    is_staff = Field(column_name=_('Staff member?'))
    is_superuser = Field(column_name=_('Is superuser?'))
    is_gpo = Field(column_name=_('Is Global Portfolio owner?'))
    # User Info
    email = Field(column_name=_('Email address'))
    name = Field(column_name=_('Name'))
    account_type = Field(column_name=_('Account type'))
    organization = Field(column_name=_('Organization'))
    country = Field(column_name=_('Country'))
    donor = Field(column_name=_('Donor'))
    language = Field(column_name=_('Language'))

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'account_type', 'organization', 'country', 'donor', 'groups', 'language',
                  'last_login', 'date_joined', 'is_odk_synced', 'is_active', 'is_staff', 'is_superuser', 'is_gpo')
        export_order = ('id', 'name', 'email', 'account_type', 'organization', 'country', 'donor', 'groups', 'language',
                        'last_login', 'date_joined', 'is_odk_synced', 'is_active', 'is_staff', 'is_superuser', 'is_gpo')

    def dehydrate_last_login(self, user: User):
        return user.last_login.date()

    def dehydrate_date_joined(self, user: User):
        return user.date_joined.date()

    def dehydrate_is_odk_synced(self, user: User):
        return user.userprofile.odk_sync

    def dehydrate_is_active(self, user: User):
        return user.is_active

    def dehydrate_is_staff(self, user: User):
        return user.is_staff

    def dehydrate_is_superuser(self, user: User):
        return user.is_superuser

    def dehydrate_is_gpo(self, user: User):
        return user.userprofile.global_portfolio_owner

    def dehydrate_name(self, user: User):
        return user.userprofile.name

    def dehydrate_email(self, user: User):
        return user.email

    def dehydrate_account_type(self, user: User):
        account_types = {x[0]: x[1] for x in UserProfile.ACCOUNT_TYPE_CHOICES}
        return account_types[user.userprofile.account_type]

    def dehydrate_organization(self, user: User):
        return user.userprofile.organisation.name if user.userprofile.organisation else 'None'

    def dehydrate_country(self, user: User):
        return user.userprofile.country.name if user.userprofile.country else 'None'

    def dehydrate_donor(self, user: User):
        return user.userprofile.donor.name if user.userprofile.donor else 'None'

    def dehydrate_language(self, user: User):
        return user.userprofile.language
