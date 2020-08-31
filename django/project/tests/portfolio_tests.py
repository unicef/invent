import copy
from datetime import datetime

import pytz
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from django.core import mail
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APIClient

from country.models import Country, Donor, CountryOffice
from project.admin import ProjectAdmin
from user.models import Organisation, UserProfile
from project.models import Project, DigitalStrategy, InteroperabilityLink, TechnologyPlatform, \
    Licence, InteroperabilityStandard, HISBucket, HSCChallenge, HSCGroup, ProjectApproval
from project.tasks import send_project_approval_digest

from project.tests.setup import SetupTests, MockRequest
from user.tests import create_profile_for_user
from project.models import Portfolio


class PortfolioTests(SetupTests):
    def setUp(self):
        super().setUp()

        self.project_data_2 = {"project": {
            "date": datetime.utcnow(),
            "name": "Test Project2",
            "organisation": self.org.id,
            "contact_name": "name1",
            "contact_email": "b@b.com",
            "implementation_overview": "overview",
            "implementation_dates": "2016",
            "health_focus_areas": [1, 2],
            "geographic_scope": "somewhere",
            "country_office": self.country_office.id,
            "platforms": [1, 2],
            "donors": [self.d1.id, self.d2.id],
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

        # Create another test user with profile.
        user_email = "test_user_gpo@unicef.org"

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
        self.test_user_2_key = response.json().get("token")
        self.test_user_2_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(self.test_user_2_key), format="json")
        self.user_2_profile_id = response.json().get('user_profile_id')

        url = reverse("userprofile-detail", kwargs={"pk": self.user_2_profile_id})
        data = {
            "name": "Test Name",
            "organisation": self.org.id,
            "country": self.country_id}
        response = self.test_user_2_client.put(url, data)
        self.assertEqual(response.status_code, 200, response.json())
        self.user_2_profile_id = response.json().get('id')

        self.userprofile_2 = UserProfile.objects.get(id=self.user_2_profile_id)
        self.country.users.add(self.userprofile_2)

        # set the userprofile to GMO
        self.userprofile_2.global_portfolio_owner = True
        self.userprofile_2.save()

        self.portfolio_data = {
            "portfolio": {
                "date": datetime.utcnow(),
                "name": "Test Portfolio",
                "description": "Test Portfolio description",
                "icon": "A",
                "managers": [self.user_profile_id],
                "projects": [self.project_id]
            }
        }

        # Create portfolio
        url = reverse("portfolio-create")
        response = self.test_user_2_client.post(url, self.portfolio_data, format="json")
        self.assertEqual(response.status_code, 201, response.json())

        self.portfolio_id = response.json()['id']

        # set portfolio to active
        url = reverse("portfolio-update", kwargs={"portfolio_id": self.portfolio_id})
        update_data = {"portfolio": {"status": Portfolio.STATUS_ACTIVE}}
        response = self.test_user_2_client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, 200, response.json())

    def test_list_portfolios(self):
        url = reverse("portfolio-list-active")
        response = self.test_user_2_client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_list_user_portfolios(self):

        url = reverse("portfolio-list")
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.test_user_2_client.get(url)
        self.assertEqual(response.status_code, 200)
