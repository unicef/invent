from scheduler.celery import app
from datetime import datetime, timedelta
from django.utils import timezone

from country.models import RegionalOffice
from .models import SolutionLog, CountryInclusionLog
from .serializers import PortfolioKPISerializer, SolutionKPISerializer


@app.task(name='solution_log_task')
def update_solution_log_task(current_date=None):
    """
    Task to update portfolio project statistics
    Needs to run daily - overwrites this month's tasks
    """
    from project.models import Portfolio, Solution

    if current_date is None:  # pragma: no cover
        current_date = timezone.now().date()

    date = current_date - timedelta(days=1)
    log_date = datetime(date.year, date.month, 1).date()
    log_entry, _ = SolutionLog.objects.get_or_create(date=log_date)

    portfolios = PortfolioKPISerializer(Portfolio.objects.all(), many=True)
    solutions = SolutionKPISerializer(Solution.objects.all(), many=True)

    log_entry.data = dict(portfolios=portfolios.data, solutions=solutions.data)
    log_entry.save()


@app.task(name='country_inclusion_log_task')
def update_country_inclusion_log_task(current_date=None):
    """
    Task to update country inclusion by regions statistics
    Needs to run daily - overwrites this month's tasks
    """
    from project.models import ProjectVersion
    from country.models import Country, CountryOffice

    if current_date is None:  # pragma: no cover
        current_date = timezone.now().date()

    date = current_date - timedelta(days=1)
    log_date = datetime(date.year, date.month, 1).date()
    log_entry, _ = CountryInclusionLog.objects.get_or_create(date=log_date)
    included_countries = Country.objects.filter(is_included=True)
    included_mco = RegionalOffice.objects.filter(is_included=True)
    max_number = included_countries.count() + included_mco.count()

    """
    Keep a tab on included objects
    inclusion = {type__object_id: True|False}
    """
    inclusion = {}
    regions = {}
    for country in included_countries:
        inclusion[f'c__{country.id}'] = False
        for region in country.regions:
            regions.setdefault(region, {})
            regions[region][f'c__{country.id}'] = False
    for mco in included_mco:
        inclusion[f'mco__{mco.id}'] = False
        for region in list(set(mco.countryoffice_set.values_list('region', flat=True))):
            regions.setdefault(region, {})
            regions[region][f'mco__{mco.id}'] = False

    """
    Fill the tab according to data
    """
    qs = ProjectVersion.objects.exclude(published=False) \
        .exclude(project__public_id='') \
        .filter(created__date__month=date.month) \
        .order_by('project_id', '-modified') \
        .distinct('project_id')
    for version in qs:
        co = CountryOffice.objects.get(id=int(version.data['country_office']))
        if not co.regional_office.is_empty_option and co.regional_office.is_included:
            inclusion[f'mco__{co.regional_office.id}'] = True
            regions[co.region][f'mco__{co.regional_office.id}'] = True
        elif co.country.is_included:
            inclusion[f'c__{co.country.id}'] = True
            regions[co.region][f'c__{co.country.id}'] = True

