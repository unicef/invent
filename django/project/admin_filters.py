from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from country.models import Country, CountryOffice


class IsPublishedFilter(admin.SimpleListFilter):
    title = _('Published')
    parameter_name = 'is_published'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.exclude(public_id__exact='')
        elif value == 'No':
            return queryset.filter(public_id__exact='')
        return queryset


class InputFilter(admin.SimpleListFilter):
    """
    Source: https://hakibenita.com/how-to-add-a-text-filter-to-django-admin
    Base class for the fancy text filter
    """
    template = 'admin/project/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):  # pragma: no cover
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class UserFilter(InputFilter):
    parameter_name = 'team'
    title = _('Team members')

    def queryset(self, request, queryset):
        term = self.value()

        if term is None:
            return

        return queryset.filter(team__name__icontains=term)


class OverViewFilter(InputFilter):
    parameter_name = 'overview'
    title = _('Overview')

    def queryset(self, request, queryset):
        term = self.value()

        if term is None:
            return

        any_name = Q()
        for bit in term.split():
            any_name &= (
                Q(data__overview__icontains=bit) |
                Q(draft__overview__icontains=bit)
            )

        return queryset.filter(any_name)


class CountryFilter(admin.SimpleListFilter):
    parameter_name = 'country'
    title = _('Country')

    def lookups(self, request, model_admin):
        qs = Country.objects.all().order_by('name').values('name', 'id')

        return ((x['id'], x['name']) for x in qs)

    def queryset(self, request, queryset):
        if self.value() is None:
            return

        term = int(self.value())

        return queryset.filter(
            Q(data__country__exact=term) |
            Q(draft__country__exact=term)
            )


class DescriptionFilter(InputFilter):
    parameter_name = 'description'
    title = _('Description')

    def queryset(self, request, queryset):
        term = self.value()

        if term is None:
            return

        return queryset.filter(
            Q(data__implementation_overview__icontains=term) |
            Q(draft__implementation_overview__icontains=term)
            )


class RegionFilter(admin.SimpleListFilter):
    parameter_name = 'region'
    title = _('Region')

    def lookups(self, request, model_admin):
        return CountryOffice.REGIONS

    def queryset(self, request, queryset):
        if self.value() is None:
            return

        term = self.value()
        office_ids = list(CountryOffice.objects.filter(region=term).values_list('id', flat=True).distinct())

        return queryset.filter(
            Q(data__country_office__in=office_ids) |
            Q(draft__country_office__in=office_ids)
            )
