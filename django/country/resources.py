from django.utils.translation import ugettext_lazy as _

from import_export import resources
from import_export.fields import Field

from .models import CountryOffice, RegionalOffice, Country


class CountryResource(resources.ModelResource):
    code = Field(column_name=_('Country Code'))
    project_approval = Field(column_name=_('Approval'))
    cover_text = Field(column_name=_('Cover text'))
    footer_title = Field(column_name=_('Footer title'))
    footer_text = Field(column_name=_('Footer text'))
    name = Field(column_name=_('Name'))
    name_fr = Field(column_name=_('French name'))
    name_pt = Field(column_name=_('Portugese name'))
    name_es = Field(column_name=_('Spanish name'))

    class Meta:
        model = Country
        fields = ('id', 'code', 'name', 'project_approval',
                  'cover_text', 'footer_title', 'footer_text',
                  'name_fr', 'name_es', 'name_pt', )
        export_order = ('id', 'code', 'name', 'project_approval',
                        'name_fr', 'name_es', 'name_pt',
                        'cover_text', 'footer_title', 'footer_text', )

    def dehydrate_code(self, country):  # pragma: no cover
        return country.code

    def dehydrate_name(self, country):  # pragma: no cover
        return country.name

    def dehydrate_name_fr(self, country):  # pragma: no cover
        return country.name_fr

    def dehydrate_name_pt(self, country):  # pragma: no cover
        return country.name_pt

    def dehydrate_name_es(self, country):  # pragma: no cover
        return country.name_es

    def dehydrate_project_approval(self, country):  # pragma: no cover
        return country.project_approval

    def dehydrate_cover_text(self, country):  # pragma: no cover
        return country.cover_text

    def dehydrate_footer_title(self, country):  # pragma: no cover
        return country.footer_title

    def dehydrate_footer_text(self, country):  # pragma: no cover
        return country.footer_text


class RegionalOfficeResource(resources.ModelResource):
    id = Field(column_name=_('ID'))
    name = Field(column_name=_('Name'))

    class Meta:
        model = RegionalOffice
        fileds = ('id', 'name')

    def dehydrate_id(self, regional_office):  # pragma: no cover
        return regional_office.id

    def dehydrate_name(self, regional_office):  # pragma: no cover
        return regional_office.name


class CountryOfficeResource(resources.ModelResource):
    name = Field(column_name=_('Name'))
    region = Field(column_name=_('Region'))
    country = Field(column_name=_('Country'))
    regional_office = Field(column_name=_('Regional office'))
    city = Field(column_name=_('City'))
    emails = Field(column_name=_('INVENT Focal Points'))

    class Meta:
        model = CountryOffice
        fields = ('name', 'region', 'country',
                  'regional_office', 'city', 'emails')
        export_order = ('name', 'region', 'country',
                        'regional_office', 'city', 'emails')

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

    # extract the emails (focal points) of user profiles as a list
    def dehydrate_emails(self, office):  # dehydrate method for export
        return ', '.join([user_profile.user.email for user_profile in office.get_user_profiles()])
