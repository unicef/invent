from django.conf import settings
from django.contrib import admin

from core.admin import AllObjectsAdmin
from .models import Country, Donor, FieldOffice, CountryOffice, RegionalOffice, Currency


# This has to stay here to use the proper celery instance with the djcelery_email package


@admin.register(Country)
class CountryAdmin(AllObjectsAdmin):
    list_display = ('name', 'code', 'project_approval')
    ordering = ('name',)
    readonly_fields = ('code', 'name')

    def get_queryset(self, request):
        return self.model.objects.all()

    def get_list_display(self, request):
        list_display = list(super(AllObjectsAdmin, self).get_list_display(request))
        language_fields = ['is_translated_{}'.format(l[0]) for l in settings.LANGUAGES]
        return list_display + language_fields

    def get_fields(self, request, obj=None):
        fields = super(CountryAdmin, self).get_fields(request, obj)
        return list(self.readonly_fields) + [f for f in fields if f not in ['name', 'code', 'map_data',
                                                                            'users', 'admins', 'super_admins',
                                                                            'lat', 'lon', 'map_activated_on',
                                                                            'region', 'unicef_region']]

    def has_add_permission(self, request):  # pragma: no cover
        return False

    def has_delete_permission(self, request, obj=None):  # pragma: no cover
        return False


@admin.register(FieldOffice)
class FieldOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_office', 'name')
    ordering = search_fields = ['country_office__name', 'name']


@admin.register(RegionalOffice)
class RegionalOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = search_fields = ['name']

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    fields = list_display = ('name', 'code')


@admin.register(CountryOffice)
class CountryOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    search_fields = ['name']
