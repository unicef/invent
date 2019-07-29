from typing import Dict, List

from django.db import models
from django.db.models import Q, QuerySet
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from django.http import QueryDict

from core.models import ExtendedModel
from project.models import Project, HealthFocusArea, DigitalStrategy
from country.models import Country, Donor
from user.models import Organisation


class ProjectSearch(ExtendedModel):
    SEARCH_BY = {
        # query_param: QuerySet param | eg: in=name&in=org
        "name": "project__name",
        "org": "organisation__name",
        "country": "country__name",
        "region": "country__unicef_region",
        "overview": "project__data__implementation_overview",
        "donor": "donor_names"
    }

    FILTER_BY = {
        # query_param: QuerySet param
        "country": "country_id",  # eg: country=1&country=2
        "sw": "software",  # eg: sw=1&sw=2
        "dhi": "dhi_categories",  # eg: dhi=1&dhi=2
        "hfa": "hfa_categories",  # eg: hfa=1&hfa=2
        "hsc": "hsc",  # eg: hsc=1&hsc=2
        "region": "country__unicef_region",  # eg: region=3
        "donor": "donors",
        "approved": "project__approval__approved",  # false=> approved=0 ; true=> approved=1
        "goal": "project__data__goal_area",  # eg: goal=1
        "result": "project__data__result_area",  # eg: result=1
        "fo": "project__data__field_office",  # eg: fo=1&fo=2
        "cl": "capability_levels",  # eg: cl=1&cl=2
        "cc": "capability_categories",  # eg: cc=1&cc=2
        "cs": "capability_subcategories",  # eg: cs=1&cs=2
    }

    project = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True, related_name='search')
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey(Organisation, null=True, on_delete=models.SET_NULL)

    donors = ArrayField(models.IntegerField(), default=list)
    donor_names = ArrayField(models.CharField(max_length=128), default=list)

    software = ArrayField(models.IntegerField(), default=list)
    dhi_categories = ArrayField(models.IntegerField(), default=list)
    hsc = ArrayField(models.IntegerField(), default=list)
    hfa_categories = ArrayField(models.IntegerField(), default=list)

    # UNICEF fields
    capability_levels = ArrayField(models.IntegerField(), default=list)
    capability_categories = ArrayField(models.IntegerField(), default=list)
    capability_subcategories = ArrayField(models.IntegerField(), default=list)

    @classmethod
    def search(cls, queryset: QuerySet, search_term: str, search_in: List[str]) -> QuerySet:
        """
        Search in QuerySet
        search_term: search term
        search_in: what field to search in
        """
        selectable_fields = set(cls.SEARCH_BY.keys())
        selected_fields = selectable_fields & set(search_in) if search_in else selectable_fields
        q = Q()

        for field in selected_fields:
            q |= Q(**{"{}__icontains".format(cls.SEARCH_BY[field]): search_term})

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
                except ValueError:
                    pass
            return lookup

        if selected_fields:
            for field in selected_fields:
                if query_params[field]:
                    if field in ["country", "region", "goal", "result", "fo"]:
                        lookup_param = "in"
                        lookup = lookup_cleanup(query_params.getlist(field))
                    elif field in ["donor", "sw", "dhi", "hfa", "hsc",
                                   "cl", "cc", "cs"]:
                        lookup_param = "overlap"  # This is the OR clause here
                        lookup = lookup_cleanup(query_params.getlist(field))
                    elif field == "approved":
                        lookup_param = "exact"
                        lookup = query_params.get(field) == '1'

                    queryset &= queryset.filter(**{"{}__{}".format(cls.FILTER_BY[field], lookup_param): lookup})

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
        if project.public_id:
            self.country_id = int(project.data["country"])
            self.organisation_id = int(project.data["organisation"])

            self.donors = [int(x) for x in project.data.get("donors", [])]
            self.donor_names = [Donor.objects.get(id=int(x)).name for x in project.data.get("donors", [])]

            self.software = project.data.get('platforms')
            self.hsc = project.data.get('hsc_challenges')
            self.dhi_categories = list(set(filter(None.__ne__,
                                                  [DigitalStrategy.get_parent_id(int(id), 'parent') for
                                                   id in project.data.get("dhis", [])])))
            self.hfa_categories = list(set(filter(None.__ne__,
                                                  [HealthFocusArea.get_parent_id(int(id), 'health_category') for
                                                   id in project.data.get("health_focus_areas", [])])))
            self.save()


@receiver(post_save, sender=Project)
def create_search_objects(sender, instance, created, **kwargs):
    if created:
        ProjectSearch.objects.get_or_create(project_id=instance.id)


@receiver(post_save, sender=Project)
def update_with_project_data(sender, instance, **kwargs):
    instance.search.update(instance)
