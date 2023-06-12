from django.core.management.base import BaseCommand
from project.models import Project
from search.models import ProjectSearch


class Command(BaseCommand):
    """
    Custom Django management command that splits 'unicef_sector' into 
    'unicef_leading_sector' and 'unicef_supporting_sectors' in both Project and 
    ProjectSearch models. 

    The 'unicef_leading_sector' field corresponds to the first element of 'unicef_sector',
    and 'unicef_supporting_sectors' field corresponds to all other elements. 
    """

    help = 'Splits sector into lead_sector and supporting_sector'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            'Splitting sectors to lead and supporting...'))
        # Iterating over all projects
        for project in Project.objects.all():
            # Checking if 'unicef_sector' field exists in project's data
            if 'unicef_sector' in project.data:
                # If it does, create a new field 'unicef_leading_sector' which is the first element of 'unicef_sector'
                # If 'unicef_sector' is empty, set 'unicef_leading_sector' as empty list
                project.data['unicef_leading_sector'] = [project.data['unicef_sector'][0]] if len(
                    project.data['unicef_sector']) > 0 else []
                # Create another new field 'unicef_supporting_sectors' which are all other elements of 'unicef_sector'
                # If 'unicef_sector' has only one or zero elements, set 'unicef_supporting_sectors' as empty list
                project.data['unicef_supporting_sectors'] = project.data['unicef_sector'][1:] if len(
                    project.data['unicef_sector']) > 1 else []
                project.save()
            # Repeat the same process for project's draft data
            if 'unicef_sector' in project.draft:
                project.draft['unicef_leading_sector'] = [project.draft['unicef_sector'][0]] if len(
                    project.draft['unicef_sector']) > 0 else []
                project.draft['unicef_supporting_sectors'] = project.draft['unicef_sector'][1:] if len(
                    project.draft['unicef_sector']) > 1 else []
                project.save()

        # Iterate over all search project records
        for search_project in ProjectSearch.objects.all():
            # Checking if 'unicef_sector' field exists in the project's data of this search project record
            if 'unicef_sector' in search_project.project.data:
                # If it does, create or update 'unicef_leading_sector' and 'unicef_supporting_sectors' fields for the search project record
                # Similar to what we did for Project records
                search_project.unicef_leading_sector = [search_project.project.data['unicef_sector'][0]] if len(
                    search_project.project.data['unicef_sector']) > 0 else []
                search_project.unicef_supporting_sectors = search_project.project.data['unicef_sector'][1:] if len(
                    search_project.project.data['unicef_sector']) > 1 else []
                search_project.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully split sector into lead_sector and supporting_sector'))
