from django.test import RequestFactory

from country.models import Country
from project.admin import ProjectAdmin
from user.models import UserProfile
from project.models import Project

from project.tests.setup import SetupTests

from project.admin_filters import IsPublishedFilter, CountryFilter, RegionFilter
from project.tests.admin_tests import TestAdmin


class TestAdminFilters(TestAdmin, SetupTests):
    def setUp(self):
        super(TestAdminFilters, self).setUp()

        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/', {})
        self.request.user = self.user
        self.projects = list()
        self.published = list()

        self.user_1_pr_id, self.user_1_client, self.user_1_key = \
            self.create_user("test_user_1@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        user_1_pr = UserProfile.objects.get(id=self.user_1_pr_id)
        user_1_pr.name = "Test User1"
        user_1_pr.save()

        self.user_2_pr_id, self.user_2_client, self.user_2_key = \
            self.create_user("test_user_2@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        user_2_pr = UserProfile.objects.get(id=self.user_2_pr_id)
        user_2_pr.name = "Test User2"
        user_2_pr.save()

        for i in range(20):
            data,  org, country, country_office, d1, d2 = self.create_test_data(name=f"Test Project {i}",
                                                                                new_country_only=(i % 3 == 0),
                                                                                convert_datetime=True)
            data['project']['country'] = country.id
            project = Project.objects.create(name=data['project']['name'], draft=data['project'])
            project.team.set([self.user_1_pr_id] if i % 2 == 0 else [self.user_2_pr_id])
            project.save()
            self.projects.append(project.id)
            if i % 2 == 0:

                project.data = project.draft
                project.make_public_id(country.id)
                project.save()
            self.published.append(project.id)

        self.admin = ProjectAdmin(Project, self.site)

    def test_admin_published_filter_choices(self):
        filter = IsPublishedFilter(None, {'published_recently': 'yes'}, Project, ProjectAdmin)
        changelist = self.admin.get_changelist_instance(self.request)
        ref_choices = [
            {'selected': True, 'query_string': '?', 'display': 'All'},
            {'selected': False, 'query_string': '?is_published=Yes', 'display': 'Yes'},
            {'selected': False, 'query_string': '?is_published=No', 'display': 'No'}
        ]

        self.assertEqual(list(filter.choices(changelist)), ref_choices)

    def test_admin_published_filter_results(self):
        request = self.request_factory.get('/?is_published=Yes', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)

        self.assertEqual(changelist.queryset.count(), 11)  # there should be 11 published projects
        request = self.request_factory.get('/?is_published=No', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 10)  # there should be 10 unpublished projects

    def test_admin_user_filter_results(self):
        request = self.request_factory.get('/?team=User1', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 10)  # there should be 10 projects with user 1

        request = self.request_factory.get('/?team=captain_caveman', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 0)  # there should be 10 projects with user 1

    def test_admin_overview_filter_results(self):
        request = self.request_factory.get('/?overview=overview', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 21)  # all projects have this data

        request = self.request_factory.get('/?team=not_overview', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 0)  # no projects have this data

    def test_admin_country_filter_choices(self):
        filter = CountryFilter(None, {'country': '0'}, Project, ProjectAdmin)
        changelist = self.admin.get_changelist_instance(self.request)
        choices = list(filter.choices(changelist))
        for choice in choices[1:]:
            country = Country.objects.get(id=int(choice['query_string'].split("=")[-1]))
            self.assertEqual(choice['display'], country.name)

    def test_admin_country_filter_results(self):
        request = self.request_factory.get(f'/?country={self.country.id}', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 14)

    def test_admin_description_filter_results(self):
        request = self.request_factory.get('/?description=overview', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 21)

        request = self.request_factory.get('/?description=overview12', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 0)

    def test_admin_region_filter_choices(self):
        filter = RegionFilter(None, {'region': '0'}, Project, ProjectAdmin)
        changelist = self.admin.get_changelist_instance(self.request)
        choices = list(filter.choices(changelist))
        regions = {x[0]: x[1] for x in Country.UNICEF_REGIONS}
        for choice in choices[1:]:
            region = regions[int(choice['query_string'].split("=")[-1])]
            self.assertEqual(choice['display'], region)

    def test_admin_region_filter_results(self):
        request = self.request_factory.get('/?region=0', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 21)

        request = self.request_factory.get('/?region=1', {})
        request.user = self.user
        changelist = self.admin.get_changelist_instance(request)
        self.assertEqual(changelist.queryset.count(), 0)
