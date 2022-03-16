from django.utils.translation import ugettext_lazy as _

from import_export import resources
from import_export.fields import Field

from .models import CountryOffice


class CountryOfficeResource(resources.ModelResource):
    name = Field(column_name=_('Name'))
    region = Field(column_name=_('Region'))
    country = Field(column_name=_('Country'))
    regional_office = Field(column_name=_('Regional office'))
    city = Field(column_name=_('City'))

    class Meta:
        model = CountryOffice
        fields = ('name', 'region', 'country', 'regional_office', 'city')
        export_order = ('name', 'region', 'country', 'regional_office', 'city')

    def dehydrate_name(self, office):  # pragma: no cover
        return office.name

    def dehydrate_region(self, office):  # pragma: no cover
        office_label = dict(office.REGIONS)[office.region]
        return office_label

    def dehydrate_country(self, office):  # pragma: no cover
        return office.country

    def dehydrate_regional_office(self, office):  # pragma: no cover
        return office.regional_office

    def dehydrate_city(self, office):  # pragma: no cover
        return office.city
