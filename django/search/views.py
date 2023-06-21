from collections import OrderedDict

from django.core.paginator import Paginator
from django.utils.functional import cached_property

from rest_framework import filters, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.views import get_object_or_400, PortfolioAccessMixin
from country.models import Donor, Country
from project.models import Portfolio, ProjectPortfolioState
from .serializers import MapResultSerializer, ListResultSerializer, PortfolioResultSerializer
from .models import ProjectSearch


class FastCountPaginator(Paginator):
    @cached_property
    def count(self):
        return len(self.object_list)


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    django_paginator_class = FastCountPaginator

    def paginate_queryset(self, queryset, request, view=None):
        max_page_size = request.query_params.get(
            self.page_size_query_param, None)
        if max_page_size is not None:
            try:
                self.max_page_size = int(max_page_size)
            except ValueError:
                max_page_size = 999999
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.page.next_page_number()
             if self.page.has_next() else None),
            ('previous', self.page.previous_page_number()
             if self.page.has_previous() else None),
            ('results', data)
        ]))


class SearchViewSet(PortfolioAccessMixin, mixins.ListModelMixin, GenericViewSet):
    search = ProjectSearch.search
    filter = ProjectSearch.filter
    found_in = ProjectSearch.found_in
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('project__name', 'project__modified', 'organisation__name',
                       'country__name', 'country_office__region', 'country_office__regional_office')
    ordering = ('-project__modified',)
    pagination_class = ResultsSetPagination
    serializer_class = ListResultSerializer

    def get_queryset(self):
        return ProjectSearch.objects.exclude(project__is_active=False) \
            .select_related('project', 'project__approval', 'organisation', 'country', 'country_office')

    def list(self, request, *args, **kwargs):
        """
        Search in projects, works by the following query params:

        ** SEARCH PARAMETERS **

        `q` search term eg: q=test  
        `in` search in [optional, defaults to all]

        ** SEARCH IN PARAMETERS **

        `id` search in initiative id, eg: in=id
        `name` search in initiative name, eg: in=name
        `overview` search in overview, eg: in=overview
        `desc` search in description, eg: in=desc
        `ach` search in current achievements, eg: in=ach
        `partner` search in partner names, eg: in=partner

        ** STANDARD FILTERS **

        `country` eg: country=1&country=2  
        `sw` eg: sw=1&sw=2  
        `dhi` eg: dhi=1&dhi=2  
        `hfa` eg: hfa=1&hfa=2  
        `hsc` eg: hsc=1&hsc=2  
        `region` eg: region=3  
        `donor` eg: donor=1&donor=2  
        `approved` eg: approved=0 (for not approved), approved=1 (for approved)  
        `stage` eg: stage=1&stage=2  
        `published` eg: published=true (for published), published=false (for not published)
        `unpublished` eg: unpublished=true (for unpublished), unpublished=false (for not unpublished)

        ** UNICEF FILTERS **

        `co` UNICEF Office eg: co=1&co=2  
        `ro` Regional Office eg: ro=1&ro=2
        `goal` Goal Area in eg: goal=1&goal=2  
        `result` Result Area in eg: result=1&result=2  
        `cl` Capability Levels overlap eg: cl=1&cl=2  
        `cc` Capability Categories overlap eg: cc=1&cc=2  
        `cs` Capability Sucategories overlap eg: cs=1&cs=2  
        `ic` Innovation Categories overlap eg: ic=1&ic=2  
        `iw` Innovation Ways eg: iw=1&iw=2  
        `us` UNICEF Sector eg: us=1&us=2  
        `hp` Hardware platforms eg: hp=1&hp=2  
        `pp` Programme Innovation/Non-Technology Platforms eg: pp=1&pp=2  
        `pf` Platform/Product Function eg: pf=1&pf=2  
        `is` Information Security Classification eg: is=1&is=2  
        `rp` Regional Priorities eg: rp=1&rp=2  

        ** PORTFOLIO FILTERS **

        `portfolio`  Portfolio in eg: portfolio=1  
        `sp` Scale Phase in eg: sp=1  
        `ps` Problem Statement in eg: ps=1  

        ** PORTFOLIO OPTIONS **

        `portfolio_page` inventory | review | portfolio (defaults to portfolio)  
        `scores`  include if present (defaults to exclude)  

        ** FOUND IN FEATURE **

        `found` include if present (defaults to exclude)  

        ** TYPE AND ORDERING **

        `type` map | list | portfolio (defaults to map) [eg: type=map]  
        `ordering` project__name | organisation__name | country__name | 
                   project__data__government_investor | country__region | 
                   project__modified  

        ** PAGINATION **

        `page` 1...n | last (will show the last page no matter the number)  
        `page_size` eg: 20  

        ** VIEW AS **

        `view_as` donor | country  

        """
        results = {}
        search_fields = set()
        donor = country = has_donor_permission = has_country_permission = None

        query_params = request.query_params

        qs = self.get_queryset()

        search_term = query_params.get('q')
        view_as = query_params.get('view_as')
        portfolio_page = query_params.get('portfolio_page', 'portfolio')
        portfolio_id = query_params.get('portfolio')

        # Add published/unpublished parameters
        published = query_params.get('published', 'true').lower()
        unpublished = query_params.get('unpublished', 'false').lower()

        # Handling invalid inputs/default values
        if published not in ['true', 'false']:
            published = 'true'
        if unpublished not in ['true', 'false']:
            unpublished = 'false'

        # Using dict-based switch-case
        query_cases = {
            ('true', 'false'): qs.exclude(project__public_id=''), # Published: yes / Unpublished: no
            ('true', 'true'): qs,  # Published: yes / Unpublished: yes
            ('false', 'true'): qs.filter(project__public_id=''), # Published: no / Unpublished: yes
            ('false', 'false'): qs.none()  # Published: no / Unpublished: no
        }
        qs = query_cases[(published, unpublished)]

        if view_as and view_as == 'donor':
            donor_list = query_params.getlist('donor')
            if not donor_list:
                raise ValidationError("No donor selected for view as.")
            elif len(donor_list) > 1:
                raise ValidationError(
                    "View as can only work with one donor selected.")

            try:
                donor = Donor.objects.get(id=int(donor_list[0]))
            except (Donor.DoesNotExist, ValueError):
                raise ValidationError("No such donor.")

            if request.user.is_superuser or donor.user_in_groups(request.user.userprofile):
                has_donor_permission = True
            else:
                raise ValidationError("No access to donor.")

        elif view_as and view_as == 'country':
            country_list = query_params.getlist('country')
            if not country_list:
                raise ValidationError("No country selected for view as.")
            elif len(country_list) > 1:
                raise ValidationError(
                    "View as can only work with one country selected.")

            try:
                country = Country.objects.get(id=int(country_list[0]))
            except (Country.DoesNotExist, ValueError):
                raise ValidationError("No such country.")

            if request.user.is_superuser or country.user_in_groups(request.user.userprofile):
                has_country_permission = True
            else:
                raise ValidationError("No access to country.")
        elif view_as:
            raise ValidationError("You can only view as country or donor.")

        if portfolio_page in ["inventory", "review"]:
            portfolio = get_object_or_400(
                Portfolio, "No such portfolio", id=portfolio_id)
            self.check_object_permissions(request, portfolio)
            query_params._mutable = True
            query_params.pop('ps', None)
            query_params.pop('sp', None)

            if portfolio_page == "inventory":
                active_reviews_for_portfolio = list(
                    ProjectPortfolioState.objects.filter(portfolio=portfolio_id).values_list('pk', flat=True))
                qs = qs.exclude(
                    project__review_states__in=active_reviews_for_portfolio)
                # edge case scenario where we need to ignore all the portfolio reliant query params from here
                query_params.pop('portfolio', None)
            elif portfolio_page == "review":
                query_params.update(dict(review=True))
            query_params._mutable = False

        if search_term:
            # 2021.10.21: DEPRECATED BECAUSE OF ID SEARCH
            # if len(search_term) < 2:
            #     raise ValidationError("Search term must be at least two characters long.")

            search_in = query_params.getlist('in')
            qs = self.search(
                queryset=qs, search_term=search_term, search_in=search_in)
            if 'found' in query_params:
                results.update(found_in=self.found_in(
                    queryset=qs, search_term=search_term))

        qs = self.filter(queryset=qs, query_params=query_params)
        qs = self.filter_queryset(qs)

        results_type = query_params.get('type', 'map')

        context = dict(donor=donor, country=country,
                       has_country_permission=has_country_permission, has_donor_permission=has_donor_permission)

        if results_type == 'list':
            page = self.paginate_queryset(qs)
            data = ListResultSerializer(page, many=True, context=context).data
        elif results_type == 'portfolio':
            if 'scores' in query_params and portfolio_page not in ["inventory", "review"]:
                portfolio = get_object_or_400(
                    Portfolio, "No such portfolio", id=portfolio_id)
                project_ids = qs.values_list('project_id', flat=True)
                results.update(
                    ambition_matrix=portfolio.get_ambition_matrix(project_ids),
                    risk_impact_matrix=portfolio.get_risk_impact_matrix(
                        project_ids),
                    problem_statement_matrix=portfolio.get_problem_statement_matrix())

            page = self.paginate_queryset(qs)

            context.update(dict(portfolio_id=portfolio_id,
                                portfolio_page=portfolio_page,
                                profile=request.user.userprofile))
            data = PortfolioResultSerializer(
                page, many=True, context=context).data
        else:
            page = self.paginate_queryset(qs)
            data = MapResultSerializer(page, many=True).data

        results.update(projects=data, type=results_type,
                       search_term=search_term, search_in=search_fields)
        return self.get_paginated_response(results)
