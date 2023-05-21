from django.conf import settings
from django.contrib import admin

from core.admin import AllObjectsAdmin
from .models import Country, Donor, CountryOffice, RegionalOffice, Currency
# ,UserProfileManagerof
from .resources import CountryOfficeResource, RegionalOfficeResource, CountryResource

from import_export.admin import ExportActionMixin


# This has to stay here to use the proper celery instance with the djcelery_email package


@admin.register(Country)
class CountryAdmin(ExportActionMixin, AllObjectsAdmin):
    resource_class = CountryResource
    list_display = ('name', 'code', 'is_included', 'regions')
    ordering = ('name',)
    readonly_fields = ('code', 'name')

    def get_queryset(self, request):
        return self.model.objects.all()

    def get_list_display(self, request):
        list_display = list(
            super(AllObjectsAdmin, self).get_list_display(request))
        language_fields = ['is_translated_{}'.format(
            l[0]) for l in settings.LANGUAGES]
        return list_display + language_fields

    def get_fields(self, request, obj=None):
        fields = super(CountryAdmin, self).get_fields(request, obj)
        return list(self.readonly_fields) + [f for f in fields if f not in ['name', 'code', 'map_data',
                                                                            'users', 'admins', 'super_admins',
                                                                            'lat', 'lon', 'map_activated_on']]

    def has_add_permission(self, request):  # pragma: no cover
        return False

    def has_delete_permission(self, request, obj=None):  # pragma: no cover
        return False

    @staticmethod
    def regions(obj):
        return [CountryOffice.REGIONS[r][1] for r in obj.regions]


@admin.register(RegionalOffice)
class RegionalOfficeAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = RegionalOfficeResource
    list_display = ('id', 'name', 'is_included', 'is_empty_option')
    ordering = search_fields = ['name']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ordering = search_fields = ['code', 'name']


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    fields = list_display = ('name', 'code')


@admin.register(CountryOffice)
class CountryOfficeAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = CountryOfficeResource
    list_display = ('id', 'name', 'region',
                    'regional_office', 'get_user_emails')
    search_fields = ['name']

    # Get the emails of user profiles in a list separated with comma iterating over them
    # utilizing the 'get_user_profiles' method in CountryOffice class
    def get_user_emails(self, obj):
        return ', '.join([user_profile.user.email for user_profile in obj.get_user_profiles()])

    # Rename this column for the interface of admin
    get_user_emails.short_description = 'INVENT Focal Points'
