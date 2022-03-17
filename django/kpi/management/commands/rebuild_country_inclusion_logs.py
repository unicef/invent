from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from datetime import datetime, date

from kpi.models import CountryInclusionLog
from kpi.tasks import update_country_inclusion_log_task


class Command(BaseCommand):
    help = 'Clears Country Inclusion KPI data and regenerates them for the past and current year'

    def handle(self, *args, **options):
        self.stdout.write("-- Clearing old data --")
        CountryInclusionLog.objects.all().delete()
        self.stdout.write("-- Generating new data --")
        generate_date = datetime(2021, 1, 2)
        while generate_date.date() <= date.today():
            self.stdout.write(f"    Date: {generate_date}")
            update_country_inclusion_log_task(generate_date)
            if generate_date.month == 12:
                generate_date = datetime(generate_date.year + 1, 1, generate_date.day)
            else:
                generate_date = datetime(generate_date.year, generate_date.month + 1, generate_date.day)
        self.stdout.write('-- Finished --')
