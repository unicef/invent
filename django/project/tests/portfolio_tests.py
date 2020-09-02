from datetime import datetime

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from project.models import Portfolio
from country.models import Country, Donor, CountryOffice
from user.models import Organisation, UserProfile
from user.tests import create_profile_for_user


class PortfolioTests(APITestCase):
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

    def create_project(self, project_name, organization, country_office, donors, user_client):
        project_data = {"project": {
            "date": datetime.utcnow(),
            "name": project_name,
            "organisation": organization.id,
            "contact_name": "name1",
            "contact_email": "a@a.com",
            "implementation_overview": "overview",
            "implementation_dates": "2016",
            "health_focus_areas": [1, 2],
            "geographic_scope": "somewhere",
            "country_office": country_office.id,
            "platforms": [1, 2],
            "donors": [donor.id for donor in donors],
            "hsc_challenges": [1, 2],
            "start_date": str(datetime.today().date()),
            "end_date": str(datetime.today().date()),
            "field_office": 1,
            "goal_area": 1,
            "result_area": 1,
            "capability_levels": [],
            "capability_categories": [],
            "capability_subcategories": [],
            "dhis": []
        }}

        # Create project draft
        url = reverse("project-create", kwargs={"country_office_id": country_office.id})
        response = user_client.post(url, project_data, format="json")
        self.assertEqual(response.status_code, 201, response.json())
        project_id = response.json().get("id")

        # Publish
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": self.country_office.id})
        response = user_client.put(url, project_data, format="json")
        self.assertEqual(response.status_code, 200, response.json())

        return project_id

    @staticmethod
    def create_portfolio(name, description, managers, projects, user_client):
        portfolio_data = {
            "date": datetime.utcnow(),
            "name": name,
            "description": description,
            "icon": "A",
            "managers": managers,
            "projects": projects,
            "problem_statements": [
                {
                    "name": "PS 1",
                    "description": "PS 1 description"
                },
                {
                    "name": "PS 2",
                    "description": "PS 2 description"
                }
            ]
        }

        # Create portfolio
        url = reverse("portfolio-create")
        return user_client.post(url, portfolio_data, format="json")

    def setUp(self):
        self.org = Organisation.objects.create(name="org1")
        self.country = Country.objects.create(name="country1", code='CTR1', project_approval=True,
                                              region=Country.REGIONS[0][0], unicef_region=Country.UNICEF_REGIONS[0][0])

        self.country_id = self.country.id
        self.country.name_en = 'Hungary'
        self.country.name_fr = 'Hongrie'
        self.country.save()

        self.country_office = CountryOffice.objects.create(
            name='Test Country Office',
            region=Country.UNICEF_REGIONS[0][0],
            country=self.country
        )
        self.d1 = Donor.objects.create(name="Donor1", code="donor1")
        self.d2 = Donor.objects.create(name="Donor2", code="donor2")

        self.user_1_pr_id, self.user_1_client, self.user_1_key = \
            self.create_user("test_user@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        self.project_1_id = self.create_project("Test Project1", self.org, self.country_office,
                                                [self.d1, self.d2], self.user_1_client)

        self.user_2_pr_id, self.user_2_client, self.user_2_key = \
            self.create_user("test_user_2@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        self.user_3_pr_id, self.user_3_client, self.user_3_key = \
            self.create_user("test_user_3@unicef.org", "123456hetNYOLC", "123456hetNYOLC")

        # set the userprofile to GMO
        self.userprofile_2 = UserProfile.objects.get(id=self.user_2_pr_id)
        self.country.users.add(self.userprofile_2)

        self.userprofile_2.global_portfolio_owner = True
        self.userprofile_2.save()

        response = self.create_portfolio("Test Portfolio 1", "Port-o-folio", [self.user_3_pr_id], [self.project_1_id],
                                         self.user_2_client)
        self.assertEqual(response.status_code, 201, response.json())

        self.portfolio_id = response.json()['id']

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
        response = self.user_1_client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, 403, response.json())

        # activate portolio as user 2, who is a GPO
        response = self.user_2_client.put(url, update_data, format="json")
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
        response = self.user_2_client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(response.json()['id'], self.portfolio_id)
        self.assertEqual(response.json()['status'], Portfolio.STATUS_DRAFT)

    def test_update_portfolio_problem_statement_fail(self):
        """
        Problem statements are handled separately
        """
        url = reverse("portfolio-update", kwargs={"pk": self.portfolio_id})
        update_data = {'problem_statements': [{"name": "PS 3", "description": "PS 3 description"}]}
        # update portolio as user 2, who is a GPO
        response = self.user_2_client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, 400, response.json())

    def test_user_create_portfolio_failed(self):
        """
        Only GMO users can create portfolios
        """
        response = self.create_portfolio("Test Portfolio 2", "Port-o-folio", [self.user_1_pr_id], [self.project_1_id],
                                         self.user_1_client)
        self.assertEqual(response.status_code, 403, response.json())

        response = self.create_portfolio("Test Portfolio 2", "Port-o-folio", [self.user_3_pr_id], [self.project_1_id],
                                         self.user_3_client)
        self.assertEqual(response.status_code, 403, response.json())

    def test_list_user_portfolios(self):
        # create another portfolio
        response = self.create_portfolio("Test Portfolio 2", "Port-o-folio", [self.user_2_pr_id], [self.project_1_id],
                                         self.user_2_client)
        self.assertEqual(response.status_code, 201, response.json())
        self.portfolio_id_2 = response.json()['id']

        url = reverse("portfolio-list")
        response = self.user_2_client.get(url)  # GMO users see all portfolios in this list
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        response = self.user_3_client.get(url)  # Managers only see their own portfolios in this list
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_detailed_portfolio_view(self):
        """
        Any user should be able to view portfolio details
        """
        url = reverse('portfolio-detailed', kwargs={"pk": self.portfolio_id})
        response = self.user_1_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.portfolio_id)
        self.assertEqual(response.json()['managers'], [self.user_3_pr_id])
        self.assertEqual(response.json()['projects'], [self.project_1_id])
        response_ps_ids = {ps['id'] for ps in response.json()['problem_statements']}
        expected_ps_ids = {ps.id for ps in Portfolio.objects.get(id=self.portfolio_id).problem_statements.all()}
        self.assertEqual(response_ps_ids, expected_ps_ids)

    def test_problem_statement_handling(self):
        """
        Managers need to be able to add and remove Problem Statements to existing portfolios
        """
        ps_data = {'problem_statement': {"name": "PS 3", "description": "PS 3 description"}}
        url = reverse('portfolio-add-problem-statement', kwargs={"pk": self.portfolio_id})
        response = self.user_3_client.post(url, ps_data, format="json")
        ps_id = response.json()['id']
        self.assertEqual(response.status_code, 201)

        url = reverse('portfolio-detailed', kwargs={"pk": self.portfolio_id})
        response = self.user_3_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['problem_statements']), 3)

        url = reverse('portfolio-delete-problem-statement', kwargs={"portfolio_id": self.portfolio_id, "pk": ps_id})
        response = self.user_3_client.delete(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('portfolio-detailed', kwargs={"pk": self.portfolio_id})
        response = self.user_3_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['problem_statements']), 2)

        for ps in response.json()['problem_statements']:
            self.assertEqual(ps['project_count'], 0)
