from datetime import datetime
from random import randint

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from country.models import Country, Donor, CountryOffice, RegionalOffice
from project.models import Stage
from user.models import Organisation, UserProfile
from user.tests import create_profile_for_user


class TestProjectData:
    def setUp(self):
        (self.project_data, self.org, self.country, self.country_office, self.d1, self.d2) = self.create_test_data(
            create_relations=True
        )

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

    @staticmethod
    def create_new_country_and_office(name: str = None, country_code: str = None, project_approval: bool = True):
        country_rand = randint(2, 9)
        if name is None:
            name = f'country{country_rand}'
        if country_code is None:
            country_code = f'CTR{country_rand}'

        country, _ = Country.objects.get_or_create(name=name, code=country_code,
                                                   project_approval=project_approval)

        country_office, _ = CountryOffice.objects.get_or_create(
            name=f'Test Country Office ({name})',
            region=CountryOffice.REGIONS[0][0],
            regional_office=RegionalOffice.objects.get_or_create(name='RO test')[0],
            country=country,
            city="Zion"
        )
        return country, country_office

    def create_test_data(self, name: str = None, create_relations: bool = False, new_country_only: bool = False,
                         convert_datetime: bool = False):
        if name is None:
            name = "Test Project1"

        if create_relations:
            org, _ = Organisation.objects.get_or_create(name="org1")

            country, country_office = self.create_new_country_and_office(
                name="country1", country_code='CTR1', project_approval=True)

            d1, _ = Donor.objects.get_or_create(name="Donor1", code="donor1")
            d2, _ = Donor.objects.get_or_create(name="Donor2", code="donor2")
        else:
            if new_country_only:
                country, country_office = self.create_new_country_and_office(project_approval=False)
            else:
                country = self.country
                country_office = self.country_office
            org = self.org
            d1 = self.d1
            d2 = self.d2

        stages = Stage.objects.all()
        return {"project": {
            "date": str(datetime.utcnow()) if convert_datetime else datetime.utcnow(),
            "name": name,
            "organisation": org.id,
            "contact_name": "name1",
            "contact_email": "a@a.com",
            "implementation_overview": "overview",
            "overview": "new overview",
            "implementation_dates": "2016",
            "health_focus_areas": [1, 2],
            "geographic_scope": "somewhere",
            "country_office": country_office.id,
            "platforms": [1, 2],
            "donors": [d1.id, d2.id],
            "hsc_challenges": [1, 2],
            "start_date": str(datetime.today().date()),
            "end_date": str(datetime.today().date()),
            "goal_area": 1,
            "result_area": 1,
            "capability_levels": [],
            "capability_categories": [],
            "capability_subcategories": [],
            "dhis": [],
            "unicef_sector": [1, 2],
            "unicef_leading_sector": [1],
            "unicef_supporting_sectors": [2],
            "innovation_categories": [1, 2],
            "cpd": [1, 2],
            "regional_priorities": [1, 2],
            "hardware": [1, 2],
            "nontech": [1, 2],
            "functions": [1, 2],
            "phase": 1,
            "partners": [dict(partner_type=0, partner_name="test partner 1", partner_email="p1@partner.ppp",
                              partner_contact="test partner contact 1", partner_website="https://partner1.com"),
                         dict(partner_type=1, partner_name="test partner 2", partner_email="p2@partner.ppp",
                              partner_contact="test partner contact 2", partner_website="https://partner2.com")],
            "links": [dict(link_type=0, link_url="https://website.com"),
                      dict(link_type=1, link_url="https://sharepoint.directory")],
            "stages": [{
                "id": stages[0].id,
                "date": str(datetime.today().date()),
                "note": "stage 1 note",
            }, {
                "id": stages[1].id,
                "date": str(datetime.today().date()),
                "note": "stage 2 note",
            }],
            "innovation_ways": [3, 2],
            "isc": 3,
            "program_targets": "program targets",
            "program_targets_achieved": "targets achieved man",
            "target_group_reached": 1,
            "current_achievements": "achieved EVERYTHING",
            "total_budget": 2000,
            "total_budget_narrative": "small amount, need more",
            "funding_needs": "yes",
            "partnership_needs": "yes please",
            "currency": 2,
            "awp": "AWP field",
            "wbs": ["WBS1", "WBS2"]
        }}, org, country, country_office, d1, d2

    def create_new_project(self, test_user_client=None, name=None, new_country_only=True):
        if test_user_client is None:
            test_user_client = self.test_user_client

        if name is None:
            project_name = f"Test Project{randint(999, 999999)}"
        else:
            project_name = name
        project_data, org, country, country_office, d1, d2 = self.create_test_data(name=project_name,
                                                                                   new_country_only=new_country_only)

        # Create project draft
        url = reverse("project-create", kwargs={"country_office_id": country_office.id})
        response = test_user_client.post(url, project_data, format="json")
        assert response.status_code == 201

        project_id = response.json().get("id")

        # Publish
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": country_office.id})
        response = test_user_client.put(url, project_data, format="json")
        assert response.status_code == 200

        return project_id, project_data, org, country, country_office, d1, d2

    @staticmethod
    def create_portfolio(name, description, managers, user_client, problem_statements=None):
        if problem_statements is None:
            problem_statements = [
                {
                    "name": "PS 1",
                    "description": "PS 1 description"
                },
                {
                    "name": "PS 2",
                    "description": "PS 2 description"
                }
            ]
        portfolio_data = {
            "date": datetime.utcnow(),
            "name": name,
            "description": description,
            "icon": "A",
            "managers": managers,
            "problem_statements": problem_statements
        }

        # Create portfolio
        url = reverse("portfolio-create")
        return user_client.post(url, portfolio_data, format="json")


class MockRequest:
    user = None
    GET = {}
    COOKIES = {}


class SetupTests(TestProjectData, APITestCase):
    def setUp(self):
        super().setUp()
        # Create a test user with profile.
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

        # Update profile.
        self.country_id = self.country.id
        self.country.name_en = 'Hungary'
        self.country.name_fr = 'Hongrie'
        self.country.save()

        url = reverse("userprofile-detail", kwargs={"pk": self.user_profile_id})
        data = {
            "name": "Test Name",
            "organisation": self.org.id,
            "country": self.country_id}
        response = self.test_user_client.put(url, data)
        self.assertEqual(response.status_code, 200, response.json())
        self.user_profile_id = response.json().get('id')

        self.userprofile = UserProfile.objects.get(id=self.user_profile_id)
        self.country.users.add(self.userprofile)

        # Create project draft
        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, self.project_data, format="json")
        self.assertEqual(response.status_code, 201, response.json())

        self.project_id = response.json().get("id")

        # Publish
        url = reverse("project-publish", kwargs={"project_id": self.project_id,
                                                 "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, self.project_data, format="json")
        self.assertEqual(response.status_code, 200, response.json())

    def check_project_search_init_state(self, project):
        obj = project.search
        self.assertEqual(obj.project_id, project.id)

        for field in obj._meta.fields:
            if field.name not in ('created', 'modified', 'project'):
                self.assertEqual(getattr(obj, field.name), field.get_default())
