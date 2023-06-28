from django.core.management.base import BaseCommand
from kpi.models import SolutionLog


class Command(BaseCommand):
    help = 'Updates solution log data for May and June 2023'

    def handle(self, *args, **options):
        may_entries = SolutionLog.objects.filter(date__year=2023, date__month=5)
        june_entries = SolutionLog.objects.filter(date__year=2023, date__month=6)

        all_entries = may_entries | june_entries

        for entry in all_entries:
            data = entry.data
            solutions = data['solutions']

            for solution in solutions:
                if 'problem_statements' in solution:
                    if isinstance(solution['problem_statements'][0], dict):
                        solution['problem_statements'] = [x['id'] for x in solution['problem_statements']]
                    solution['problem_statements'] = list(set(solution['problem_statements']))
                
                if 'portfolios' in solution:
                    if isinstance(solution['portfolios'][0], dict):
                        solution['portfolios'] = [x['id'] for x in solution['portfolios']]
                    solution['portfolios'] = list(set(solution['portfolios']))

            entry.data = data
            entry.save()