from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from project.models import Portfolio, ProblemStatement
from project.tests.setup import TestProjectData
from user.models import UserProfile
from user.tests import create_profile_for_user


class PortfolioSetup(TestProjectData, APITestCase):
    def create_user(self, user_email, user_password1, user_password_2):
        """
        Create a test user with profile.
        """
        url = reverse("rest_register")
        data = {
            "email": user_email,
            "password1": user_password1,
            "password2": user_password_2}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201, response.json())

        create_profile_for_user(response)

        # Log in the user.
        url = reverse("api_token_auth")
        data = {
            "username": user_email,
            "password": user_password1}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200, response.json())
        test_user_key = response.json().get("token")
        test_user_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(test_user_key), format="json")
        user_profile_id = response.json().get('user_profile_id')
        return user_profile_id, test_user_client, test_user_key

    def move_project_to_portfolio(self, portfolio_id, project_id, expected_response_status=201, client=None):
        if client is None:
            client = self.user_3_client
        url = reverse("portfolio-project-add", kwargs={"pk": portfolio_id})
        request_data = {"project": [project_id]}

        # check permissions with user_1_client, which is not allowed
        response = client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, expected_response_status, response.json())
        return response.json()

    def review_and_approve_project(self, pps, scores, client=None):
        if client is None:
            client = self.user_3_client  # pragma: no cover
        url = reverse('portfolio-project-manager-review', kwargs={'pk': pps.id})
        response = client.post(url, scores, format="json")
        self.assertEqual(response.status_code, 200, f'{response.json()}')

        project_id = pps.project.id

        url = reverse('portfolio-project-approve', kwargs={'pk': pps.portfolio.id})
        response = self.user_3_client.post(url, {'project': [project_id]}, format="json")
        self.assertEqual(response.status_code, 200, f'{response.json()}')
        return response.json()

    def setUp(self):
        super().setUp()

        self.user_1_pr_id, self.user_1_client, self.user_1_key = \
            self.create_user("test_user_1@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        self.project_1_id, project_data, org, country, country_office, d1, d2 = \
            self.create_new_project(self.user_1_client)

        self.user_2_pr_id, self.user_2_client, self.user_2_key = \
            self.create_user("test_user_2@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        self.user_3_pr_id, self.user_3_client, self.user_3_key = \
            self.create_user("test_user_3@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        # set the userprofile to GMO
        self.userprofile_2 = UserProfile.objects.get(id=self.user_2_pr_id)
        self.country.users.add(self.userprofile_2)

        self.userprofile_2.global_portfolio_owner = True
        self.userprofile_2.save()

        response = self.create_portfolio("Test Portfolio 1", "Port-o-folio", [self.user_3_pr_id], self.user_2_client)
        self.assertEqual(response.status_code, 201, response.json())
        self.portfolio_id = response.json()['id']


class PortfolioTests(PortfolioSetup):

    def test_list_portfolios(self):
        """
        Homepage will display the name and a brief description of each of the active portfolios within the tool.
        When the user clicks on a portfolio, they will be directed to the corresponding portfolio view page.
        As any user persona, I want to be able to view information about UNICEF’s portfolio approach
        and the active portfolios.
        """
        url = reverse("portfolio-list-active")
        response = self.user_1_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)  # we forgot to activate the portfolio
        # Try to set the portfolio to active as user #1, who is not allowed
        url = reverse("portfolio-update", kwargs={"pk": self.portfolio_id})
        update_data = {"status": Portfolio.STATUS_ACTIVE}
        response = self.user_1_client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, 403, response.json())

        # activate portolio as user 2, who is a GPO
        response = self.user_2_client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(response.json()['id'], self.portfolio_id)
        self.assertEqual(response.json()['status'], Portfolio.STATUS_ACTIVE)

        # Re-check the portfolio list as user #1
        url = reverse("portfolio-list-active")
        response = self.user_1_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)  # we forgot to activate the portfolio
        self.assertEqual(response.json()[0]['id'], self.portfolio_id)

        # Make the portfolio a draft again
        url = reverse("portfolio-update", kwargs={"pk": self.portfolio_id})
        update_data = {"status": Portfolio.STATUS_DRAFT}
        response = self.user_2_client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(response.json()['id'], self.portfolio_id)
        self.assertEqual(response.json()['status'], Portfolio.STATUS_DRAFT)

    def test_user_create_portfolio_failed(self):
        """
        Only GMO users can create portfolios
        """
        response = self.create_portfolio("Test Portfolio 2", "Port-o-folio", [self.user_1_pr_id], self.user_1_client)
        self.assertEqual(response.status_code, 403, response.json())

        response = self.create_portfolio("Test Portfolio 2", "Port-o-folio", [self.user_3_pr_id], self.user_3_client)
        self.assertEqual(response.status_code, 403, response.json())

    def test_list_user_portfolios(self):
        # create another portfolio
        response = self.create_portfolio("Test Portfolio 2", "Port-o-folio", [self.user_2_pr_id], self.user_2_client)
        self.assertEqual(response.status_code, 201, response.json())
        self.portfolio_id_2 = response.json()['id']

        url = reverse("portfolio-list")
        response = self.user_2_client.get(url)  # GMO users see all portfolios in this list
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        response = self.user_3_client.get(url)  # Managers only see their own portfolios in this list
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_problem_statement_handling(self):
        """
        Managers need to be able to add, update and remove Problem Statements to existing portfolios
        """
        ps_1 = ProblemStatement.objects.get(name="PS 1")
        ps_2 = ProblemStatement.objects.get(name="PS 2")

        url = reverse("portfolio-update", kwargs={"pk": self.portfolio_id})
        update_data = {'problem_statements': [
            {'id': ps_1.id, 'name': "PS 1 updated", 'description': ps_1.description},
            {'name': "PS 3", 'description': "This was added recently"}]}

        response = self.user_3_client.patch(url, update_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['problem_statements']), 2)
        expected_names = {"PS 1 updated", "PS 3"}
        response_names = {ps['name'] for ps in response.json()['problem_statements']}
        self.assertEqual(response_names, expected_names)
        ps_3 = ProblemStatement.objects.get(name="PS 3")
        self.assertNotEqual(ps_3.id, ps_2.id)  # Check that we've actually created a new Problem Statement
        ps_1_recheck = ProblemStatement.objects.get(id=ps_1.id)
        self.assertEqual(ps_1_recheck.name, "PS 1 updated")

    def test_remove_problem_statements(self):
        url = reverse("portfolio-update", kwargs={"pk": self.portfolio_id})
        update_data = {'name': 'Port-O-Folio ultra updated', 'problem_statements': []}

        response = self.user_3_client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()['problem_statements']), 0)
        self.assertEqual(response.json()['name'], 'Port-O-Folio ultra updated')

    def test_add_and_remove_managers(self):
        # create a brand new user to be a new manager
        user_4_pr_id, user_4_client, user_4_key = \
            self.create_user("the_new_guy@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        portfolio = Portfolio.objects.get(id=self.portfolio_id)
        managers = list(portfolio.managers.values_list('id', flat=True))
        managers.append(user_4_pr_id)

        url = reverse("portfolio-update", kwargs={"pk": self.portfolio_id})
        update_data = {'managers': managers}

        response = self.user_3_client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()['managers']), set(managers))
        user_4_profile = UserProfile.objects.get(id=user_4_pr_id)

        self.assertEqual(list(user_4_profile.portfolios.all().values_list('id', flat=True)), [self.portfolio_id])

        update_data = {'managers': [self.user_3_pr_id]}

        # user 4 removes themselves from being managers
        response = user_4_client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(set(response.json()['managers']), {self.user_3_pr_id})
        user_4_profile = UserProfile.objects.get(id=user_4_pr_id)
        self.assertEqual(list(user_4_profile.portfolios.all().values_list('id', flat=True)), [])
