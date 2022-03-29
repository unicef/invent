from copy import copy
from datetime import date, timedelta

from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse

from country.models import Country, CountryOffice, Donor, RegionalOffice
from project.models import Portfolio, Solution, ProblemStatement, CountrySolution, ProjectVersion, Project
from project.tests.setup import TestProjectData
from user.models import UserProfile, Organisation
from user.tests import create_profile_for_user
from .models import CountryInclusionLog

from .tasks import update_solution_log_task, update_country_inclusion_log_task


class SolutionKPITests(TestProjectData, APITestCase):
    def setUp(self):
        user_email = "test_user@unicef.org"

        url = reverse("rest_register")
        data = {
            "email": user_email,
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201, response.json())

        create_profile_for_user(response)

        # Log in the user.
        url = reverse("api_token_auth")
        data = {
            "username": user_email,
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200, response.json())
        self.test_user_key = response.json().get("token")
        self.test_user_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(self.test_user_key), format="json")
        self.user_profile_id = response.json().get('user_profile_id')

        self.userprofile = UserProfile.objects.get(id=self.user_profile_id)
        self.userprofile.global_portfolio_owner = True
        self.userprofile.save()

        self.org, _ = Organisation.objects.get_or_create(name="org1")
        self.d1, _ = Donor.objects.get_or_create(name="Donor1", code="donor1")
        self.d2, _ = Donor.objects.get_or_create(name="Donor2", code="donor2")

    def test_solutions_kpi_two_snapshot_differences(self):
        self.port1_resp = self.create_portfolio(name='Test Portfolio 1', description='Testing solutions 1',
                                                user_client=self.test_user_client, managers=[self.user_profile_id])
        self.port2_resp = self.create_portfolio(name='Test Portfolio 2', description='Testing solutions 2',
                                                user_client=self.test_user_client, managers=[self.user_profile_id])

        self.country_1 = Country.objects.all()[0]
        self.country_2 = Country.objects.all()[1]
        ps_1 = ProblemStatement.objects.all()[0]
        ps_2 = ProblemStatement.objects.all()[1]
        self.sol_1 = Solution.objects.create(
            name="Solution 1", phase=Solution.PHASES[0][0], open_source_frontier_tech=False,
            learning_investment=True
        )
        CountrySolution.objects.create(country=self.country_1, solution=self.sol_1, region=CountryOffice.REGIONS[0][0],
                                       people_reached=100)
        CountrySolution.objects.create(country=self.country_2, solution=self.sol_1, region=CountryOffice.REGIONS[1][0],
                                       people_reached=23)

        self.assertEqual(Portfolio.objects.get(id=self.port1_resp.json()['id']).landscape_review, False)
        self.assertEqual(Portfolio.objects.get(id=self.port2_resp.json()['id']).landscape_review, False)

        self.sol_1.portfolios.set([self.port1_resp.json()['id'], self.port2_resp.json()['id']])
        self.sol_1.problem_statements.set([ps_1, ps_2])
        self.sol_2 = Solution.objects.create(
            name="Solution 2", phase=Solution.PHASES[1][0], open_source_frontier_tech=True, learning_investment=True
        )
        CountrySolution.objects.create(country=self.country_1, solution=self.sol_2, region=CountryOffice.REGIONS[3][0],
                                       people_reached=400)
        self.sol_2.portfolios.set([self.port1_resp.json()['id']])
        self.sol_2.problem_statements.set([ps_1, ps_2])

        generate_date = date.today() - timedelta(days=30)
        update_solution_log_task(generate_date)

        port2 = Portfolio.objects.get(id=self.port2_resp.json()['id'])
        port2.status = Portfolio.STATUS_ACTIVE
        port2.investment_to_date = 999
        port2.save()

        CountrySolution.objects.create(country=self.country_2, solution=self.sol_2, region=CountryOffice.REGIONS[3][0],
                                       people_reached=56)
        self.sol_2.portfolios.set([self.port1_resp.json()['id'], self.port2_resp.json()['id']])

        generate_date = generate_date + timedelta(days=30)
        update_solution_log_task(generate_date)

        url = reverse("solutions-kpi-list")
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        past_snapshot = response.json()[0]['data']
        current_snapshot = response.json()[1]['data']

        self.assertEqual(past_snapshot['portfolios'][0]['status'], current_snapshot['portfolios'][0]['status'])
        self.assertNotEqual(past_snapshot['portfolios'][1]['status'], current_snapshot['portfolios'][1]['status'])
        self.assertNotEqual(past_snapshot['portfolios'][1]['investment_to_date'],
                            current_snapshot['portfolios'][1]['investment_to_date'])
        self.assertNotEqual(past_snapshot['portfolios'][1]['solutions'], current_snapshot['portfolios'][1]['solutions'])
        self.assertNotEqual(past_snapshot['solutions'][1]['countries'], current_snapshot['solutions'][1]['countries'])
        self.assertNotEqual(past_snapshot['solutions'][1]['portfolios'], current_snapshot['solutions'][1]['portfolios'])
        self.assertEqual(past_snapshot['solutions'][1]['people_reached'], 400)
        self.assertEqual(current_snapshot['solutions'][1]['people_reached'], 456)
        self.assertEqual(past_snapshot['solutions'][0]['regions'],
                         [CountryOffice.REGIONS[0][0], CountryOffice.REGIONS[1][0]])
        self.assertEqual(self.sol_1.regions_display, [CountryOffice.REGIONS[0][1], CountryOffice.REGIONS[1][1]])

    def test_country_inclusions_by_regions(self):
        self.country, _ = Country.objects.get_or_create(name='Test Country Inclusion', code='XY',
                                                        project_approval=False, is_included=True)
        region = CountryOffice.REGIONS[0][0]
        self.country_office, _ = CountryOffice.objects.get_or_create(
            name='Test Country Office',
            region=region,
            regional_office=RegionalOffice.objects.get_or_create(name='RO test')[0],
            country=self.country,
            city="Zion"
        )

        project_id, project_data, org, country, country_office, d1, d2 = self.create_new_project(
            new_country_only=False)
        project = Project.objects.get(id=project_id)

        new_country, _ = Country.objects.get_or_create(name='Test Country Inclusion 2', code='XYX',
                                                       project_approval=False, is_included=True)
        new_region = CountryOffice.REGIONS[1][0]
        new_country_office, _ = CountryOffice.objects.get_or_create(
            name='Test Country Office2',
            region=new_region,
            regional_office=RegionalOffice.objects.get_or_create(name='RO test')[0],
            country=new_country,
            city="Zion"
        )
        new_data = copy(project.data)
        new_data['country_office'] = new_country_office.id

        ProjectVersion.objects.create(project=project, user=self.userprofile, name=project.name,
                                      data=new_data, published=True)

        update_country_inclusion_log_task(current_date=timezone.now().date() + timedelta(days=1))
        log = CountryInclusionLog.objects.get()

        self.assertEqual(log.data['countries'], 1)
        self.assertEqual(log.data['max_countries'], 2)
        self.assertEqual(log.data['regions'][0]['countries'], 0)
        self.assertEqual(log.data['regions'][0]['max_countries'], 1)
        self.assertEqual(log.data['regions'][1]['countries'], 1)
        self.assertEqual(log.data['regions'][1]['max_countries'], 1)
        self.assertEqual(log.data['regions'][1]['id'], new_region)
        self.assertNotEqual(log.data['regions'][1]['id'], region)

        new_regional_office, _ = RegionalOffice.objects.get_or_create(name='RO inclusion test', is_included=True)
        new_region = CountryOffice.REGIONS[2][0]
        new_country_office, _ = CountryOffice.objects.get_or_create(
            name='Test Country Office3',
            region=new_region,
            regional_office=new_regional_office,
            country=new_country,
            city="Zion"
        )
        new_data['country_office'] = new_country_office.id

        ProjectVersion.objects.create(project=project, user=self.userprofile, name=project.name,
                                      data=new_data, published=True)

        update_country_inclusion_log_task(current_date=timezone.now().date() + timedelta(days=1))
        log.refresh_from_db()

        self.assertEqual(log.data['countries'], 1)
        self.assertEqual(log.data['max_countries'], 3)
        self.assertEqual(log.data['regions'][0]['countries'], 0)
        self.assertEqual(log.data['regions'][0]['max_countries'], 1)
        self.assertEqual(log.data['regions'][1]['countries'], 0)
        self.assertEqual(log.data['regions'][1]['max_countries'], 1)
        self.assertEqual(log.data['regions'][2]['id'], new_region)
        self.assertEqual(log.data['regions'][2]['countries'], 1)
        self.assertEqual(log.data['regions'][2]['max_countries'], 2)
        self.assertEqual(len(new_country.regions), 2)

        url = reverse("country-inclusion-kpi-list")
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(log.data, response.json()[0]['data'])

    def test_country_inclusion_aggregations_by_month(self):
        self.country, _ = Country.objects.get_or_create(name='Test Country Inclusion', code='XY',
                                                        project_approval=False, is_included=True)
        region = CountryOffice.REGIONS[0][0]
        self.country_office, _ = CountryOffice.objects.get_or_create(
            name='Test Country Office',
            region=region,
            regional_office=RegionalOffice.objects.get_or_create(name='RO test')[0],
            country=self.country,
            city="Zion"
        )

        self.create_new_project(new_country_only=False)

        project_id_2, project_data_2, org, country, country_office, d1, d2 = self.create_new_project(
            new_country_only=False)
        project_2 = Project.objects.get(id=project_id_2)

        new_country, _ = Country.objects.get_or_create(name='Test Country Inclusion 2', code='XYX',
                                                       project_approval=False, is_included=True)
        region = CountryOffice.REGIONS[0][0]
        new_country_office, _ = CountryOffice.objects.get_or_create(
            name='Test Country Office2',
            region=region,
            regional_office=RegionalOffice.objects.get_or_create(name='RO test')[0],
            country=new_country,
            city="Zion"
        )
        new_data = copy(project_2.data)
        new_data['country_office'] = new_country_office.id

        ProjectVersion.objects.create(project=project_2, user=self.userprofile, name=project_2.name,
                                      data=new_data, published=True)

        future_date = timezone.now() + timedelta(days=60)
        project_2.versions.filter(published=True).update(created=future_date)

        update_country_inclusion_log_task(current_date=timezone.now().date() + timedelta(days=1))
        log = CountryInclusionLog.objects.get()

        self.assertEqual(log.data['countries'], 1)
        self.assertEqual(log.data['max_countries'], 2)
        self.assertEqual(log.data['regions'][0]['countries'], 1)
        self.assertEqual(log.data['regions'][0]['max_countries'], 2)

        project_id_3, project_data_3, org, country, country_office, d1, d2 = self.create_new_project(
            new_country_only=False)
        project_3 = Project.objects.get(id=project_id_3)

        new_country, _ = Country.objects.get_or_create(name='Test Country Inclusion 3', code='XY2',
                                                       project_approval=False, is_included=True)
        new_country_office, _ = CountryOffice.objects.get_or_create(
            name='Test Country Office3',
            region=region,
            regional_office=RegionalOffice.objects.get_or_create(name='RO test')[0],
            country=new_country,
            city="Zion"
        )
        new_data = copy(project_3.data)
        new_data['country_office'] = new_country_office.id

        ProjectVersion.objects.create(project=project_3, user=self.userprofile, name=project_3.name,
                                      data=new_data, published=True)

        past_date = timezone.now() - timedelta(days=120)
        project_3.versions.filter(published=True).update(created=past_date)

        update_country_inclusion_log_task(current_date=timezone.now().date() + timedelta(days=1))
        log.refresh_from_db()

        self.assertEqual(log.data['countries'], 2)
        self.assertEqual(log.data['max_countries'], 3)
        self.assertEqual(log.data['regions'][0]['countries'], 2)
        self.assertEqual(log.data['regions'][0]['max_countries'], 3)

        project_2.versions.filter(published=True).update(created=past_date)
        update_country_inclusion_log_task(current_date=timezone.now().date() + timedelta(days=1))
        log.refresh_from_db()

        self.assertEqual(log.data['countries'], 3)
        self.assertEqual(log.data['max_countries'], 3)
        self.assertEqual(log.data['regions'][0]['countries'], 3)
        self.assertEqual(log.data['regions'][0]['max_countries'], 3)
