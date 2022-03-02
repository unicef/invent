from scheduler.celery import app
from datetime import datetime, timedelta
from django.utils import timezone

from .models import SolutionLog
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
