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
