from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from project.models import Project


class Command(BaseCommand):
    help = 'Removes 1970 unix epoch dates that were falsely saves in the DB.'

    def handle(self, *args, **options):
        draft_end = Project.objects.filter(draft__end_date__icontains='1970')
        data_end = Project.objects.filter(data__end_date__icontains='1970')
        draft_start = Project.objects.filter(draft__start_date__icontains='1970')
        data_start = Project.objects.filter(data__start_date__icontains='1970')

        print(f'Updating start date for {draft_start.count()} draft projects')
        for p in draft_start:
            p.draft['start_date'] = ''
            p.save(update_fields=['draft'])

        print(f'Updating start date for {data_start.count()} published projects')
        for p in data_start:
            p.data['start_date'] = ''
            p.save(update_fields=['data'])

        print(f'Updating end date for {draft_end.count()} draft projects')
        for p in draft_end:
            p.draft['end_date'] = ''
            p.save(update_fields=['draft'])

        print(f'Updating end date for {data_end.count()} published projects')
        for p in data_end:
            p.data['end_date'] = ''
            p.save(update_fields=['data'])
