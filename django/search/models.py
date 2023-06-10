from typing import Dict, List

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q, QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import QueryDict

from core.models import ExtendedModel
from country.models import Country, CountryOffice
from project.models import Project, HealthFocusArea, DigitalStrategy, ProjectPortfolioState
from user.models import Organisation


class ProjectSearch(ExtendedModel):
    SEARCH_BY = {
        # query_param: QuerySet param | eg: in=name&in=overview
        "id": "project__id",
        "name": "project__name",
        "overview": "project__data__implementation_overview",
        "desc": "project__data__overview",
        "ach": "project__data__current_achievements",
        "partner": "partner_names",
        # DEPRECATION WARNING: still used on the landing page search
        "org": "organisation__name",
        "co": "country_office__name",
        "country": "country__name",
        "region": "country_office__region",
    }

    FILTER_BY = {
        # query_param: QuerySet param
        "co": "country_office_id",
        "country": "country_id",
        "sw": "software",
        "dhi": "dhi_categories",
        "hfa": "hfa_categories",
        "hsc": "hsc",
        "region": "country_office__region",
        "donor": "donors",
        "approved": "project__approval__approved",
        "goal": "project__data__goal_area",
        "result": "project__data__result_area",
        "cl": "capability_levels",
        "cc": "capability_categories",
        "cs": "capability_subcategories",
        "ic": "innovation_categories",
        "portfolio": "project__review_states",
        "ro": "country_office__regional_office",
        "stage": "project__data__current_phase",
        "iw": "innovation_ways",
        "us": "unicef_sector",
        "hp": "hardware",
        "pp": "nontech",
        "pf": "functions",
        "is": "project__data__isc",
        "rp": "regional_priorities",
    }

    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, primary_key=True, related_name='search')
    country_office = models.ForeignKey(
        CountryOffice, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey(
        Organisation, null=True, on_delete=models.SET_NULL)

    donors = ArrayField(models.IntegerField(), default=list)
    partner_names = models.TextField(null=True, blank=True)

    software = ArrayField(models.IntegerField(), default=list)
    dhi_categories = ArrayField(models.IntegerField(), default=list)
    hsc = ArrayField(models.IntegerField(), default=list)
    hfa_categories = ArrayField(models.IntegerField(), default=list)

    # UNICEF fields
    capability_levels = ArrayField(models.IntegerField(), default=list)
    capability_categories = ArrayField(models.IntegerField(), default=list)
    capability_subcategories = ArrayField(models.IntegerField(), default=list)
    innovation_categories = ArrayField(models.IntegerField(), default=list)
    innovation_ways = ArrayField(models.IntegerField(), default=list)
    unicef_sector = ArrayField(models.IntegerField(), default=list)
    unicef_leading_sector = ArrayField(models.IntegerField(), default=list)
    unicef_supporting_sectors = ArrayField(models.IntegerField(), default=list)
    hardware = ArrayField(models.IntegerField(), default=list)
    nontech = ArrayField(models.IntegerField(), default=list)
    functions = ArrayField(models.IntegerField(), default=list)
    regional_priorities = ArrayField(models.IntegerField(), default=list)

    @classmethod
    def search(cls, queryset: QuerySet, search_term: str, search_in: List[str]) -> QuerySet:
        """
        Search in QuerySet
        search_term: search term
        search_in: what field to search in
        """
        selectable_fields = set(cls.SEARCH_BY.keys())
        selected_fields = selectable_fields & set(
            search_in) if search_in else selectable_fields
        q = Q()

        for field in selected_fields:
            if field == "id":
                try:
                    search_id = int(search_term)
                except ValueError:
                    pass
                else:
                    q |= Q(
                        **{"{}__exact".format(cls.SEARCH_BY[field]): search_id})
            else:
                q |= Q(
                    **{"{}__icontains".format(cls.SEARCH_BY[field]): search_term})

        return queryset.filter(q) if selected_fields else queryset

    @classmethod
    def filter(cls, queryset: QuerySet, query_params: QueryDict) -> QuerySet:
        """
        Filter QuerySet by various filter terms
        """
        selectable_fields = set(cls.FILTER_BY.keys())
        selected_fields = set(query_params.keys()) & selectable_fields
        lookup = lookup_param = None

        def lookup_cleanup(values: list) -> List[int]:  # keep ints only
            lookup = []
            for value in values:
                try:
                    lookup.append(int(value))
                except ValueError:  # pragma: no cover
                    pass
            return lookup

        if selected_fields:
            for field in selected_fields:
                if query_params[field]:
                    if field in ["country", "co", "region", "goal", "result", "ro", "is", "stage"]:
                        lookup_param = "in"
                        lookup = lookup_cleanup(query_params.getlist(field))
                    elif field in ["donor", "sw", "dhi", "hfa", "hsc",
                                   "cl", "cc", "cs", "ic",
                                   "iw", "us", "hp", "pp", "pf", "rp"]:
                        lookup_param = "overlap"  # This is the OR clause here
                        lookup = lookup_cleanup(query_params.getlist(field))
                    elif field == "approved":
                        lookup_param = "exact"
                        lookup = query_params.get(field) == '1'
                    elif field == "portfolio":
                        filter_params = dict(scale_phase=query_params.get('sp'),
                                             portfolio_id=query_params.get(
                                                 'portfolio'),
                                             psa=query_params.get('ps'),
                                             approved=not query_params.get('review', False))
                        pps_filter_params = {
                            k: v for k, v in filter_params.items() if v is not None}
                        lookup_param = "in"
                        lookup = list(ProjectPortfolioState.objects.filter(**pps_filter_params)
                                      .values_list('pk', flat=True))

                        if not lookup:
                            return queryset.none()

                    queryset &= queryset.filter(
                        **{"{}__{}".format(cls.FILTER_BY[field], lookup_param): lookup})
        return queryset

    @classmethod
    def found_in(cls, queryset: QuerySet, search_term: str) -> Dict[str, list]:
        """
        Returns what projects are found in which search field
        {
            field: [project_id(s)]
        }
        """
        found_in = {}

        for field, exp in cls.SEARCH_BY.items():
            project_ids = queryset.filter(**{"{}__icontains".format(exp): search_term})\
                .values_list('project_id', flat=True)
            found_in[field] = project_ids

        return found_in

    def update(self, project: Project):
        """
        Update search object from project object
        """
        if project.public_id and project.is_active:
            self.country_office_id = int(project.data.get("country_office")) \
                if project.data.get("country_office") else None
            self.country_id = int(project.data["country"])
            self.organisation_id = int(project.data["organisation"])

            self.donors = [int(x) for x in project.data.get("donors", [])]

            self.software = project.data.get('platforms')
            self.hsc = project.data.get('hsc_challenges')
            self.dhi_categories = list(set(filter(None.__ne__,
                                                  [DigitalStrategy.get_parent_id(int(id), 'parent') for
                                                   id in project.data.get("dhis", [])])))
            self.hfa_categories = list(set(filter(None.__ne__,
                                                  [HealthFocusArea.get_parent_id(int(id), 'health_category') for
                                                   id in project.data.get("health_focus_areas", [])])))
            self.capability_levels = project.data.get('capability_levels')
            self.capability_categories = project.data.get(
                'capability_categories')
            self.capability_subcategories = project.data.get(
                'capability_subcategories')
            self.innovation_categories = project.data.get(
                'innovation_categories', [])
            self.innovation_ways = project.data.get('innovation_ways', [])
            self.unicef_sector = project.data.get('unicef_sector', [])
            self.unicef_leading_sector = project.data.get(
                'unicef_leading_sector', [])
            self.unicef_supporting_sectors = project.data.get(
                'unicef_supporting_sectors', [])
            self.hardware = project.data.get('hardware', [])
            self.nontech = project.data.get('nontech', [])
            self.functions = project.data.get('functions', [])
            self.regional_priorities = project.data.get(
                'regional_priorities', [])
            self.partner_names = ", ".join([x.get('partner_name', "") for x in project.data.get("partners")]) \
                if project.data.get("partners") else ""
            self.save()

    def reset(self):
        for field in self._meta.fields:
            if field.name not in ('created', 'modified', 'project'):
                setattr(self, field.name, field.get_default())
        self.save()


@receiver(post_save, sender=Project)
def create_search_objects(sender, instance, created, **kwargs):
    if created:
        ProjectSearch.objects.get_or_create(project_id=instance.id)


@receiver(post_save, sender=Project)
def remove_search_objects(sender, instance, **kwargs):  # pragma: no cover
    if not instance.is_active and getattr(instance, 'search', None):
        instance.search.reset()


@receiver(post_save, sender=Project)
def update_with_project_data(sender, instance, **kwargs):
    if instance.is_active and instance.public_id and getattr(instance, 'search', None):
        instance.search.update(instance)
