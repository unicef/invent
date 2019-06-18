from datetime import datetime

from allauth.account.models import EmailConfirmation
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from country.models import Country, Donor
from user.models import Organisation, UserProfile


class MockRequest():
    user = None
    GET = {}
    COOKIES = {}


class SetupTests(APITestCase):
    def setUp(self):
        # Create a test user with profile.
        url = reverse("rest_register")
        data = {
            "email": "test_user@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201, response.json())

        # Validate the account.
        key = EmailConfirmation.objects.get(email_address__email="test_user@gmail.com").key
        url = reverse("rest_verify_email")
        data = {
            "key": key,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200, response.json())

        # Log in the user.
        url = reverse("api_token_auth")
        data = {
            "username": "test_user@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200, response.json())
        self.test_user_key = response.json().get("token")
        self.test_user_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(self.test_user_key), format="json")
        self.user_profile_id = response.json().get('user_profile_id')

        # Update profile.
        self.org = Organisation.objects.create(name="org1")
        self.country = Country.objects.create(name="country1", code='CTR1', project_approval=True,
                                              region=Country.REGIONS[0][0])
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

        self.d1 = Donor.objects.create(name="Donor1", code="donor1")
        self.d2 = Donor.objects.create(name="Donor2", code="donor2")

        self.project_data = {"project": {
            "date": datetime.utcnow(),
            "name": "Test Project1",
            "organisation": self.org.id,
            "contact_name": "name1",
            "contact_email": "a@a.com",
            "implementation_overview": "overview",
            "implementation_dates": "2016",
            "health_focus_areas": [1, 2],
            "geographic_scope": "somewhere",
            "country": self.country_id,
            "platforms": [{
                "id": 1,
                "strategies": [1, 2]
            }, {
                "id": 2,
                "strategies": [1, 9]
            }],
            "licenses": [1, 2],
            "coverage": [
                {"district": "dist1", "clients": 20, "health_workers": 5, "facilities": 4},
                {"district": "dist2", "clients": 10, "health_workers": 2, "facilities": 8}
            ],
            "coverage_second_level": [
                {"district": "ward1", "clients": 209, "health_workers": 59, "facilities": 49},
                {"district": "ward2", "clients": 109, "health_workers": 29, "facilities": 89}
            ],
            "national_level_deployment":
                {"clients": 20000, "health_workers": 0, "facilities": 0,
                 "facilities_list": ['facility1', 'facility2', 'facility3']},
            "donors": [self.d1.id, self.d2.id],
            "his_bucket": [1, 2],
            "hsc_challenges": [1, 2],
            "government_investor": 0,
            "implementing_partners": ["partner1", "partner2"],
            "repository": "http://some.repo",
            "mobile_application": "http://mobile.app.org",
            "wiki": "http://wiki.org",
            "interoperability_links": [{"id": 1, "selected": True, "link": "http://blabla.com"},
                                       {"id": 2, "selected": True},
                                       {"id": 3, "selected": True, "link": "http://example.org"}],
            "interoperability_standards": [1],
            "start_date": str(datetime.today().date()),
            "end_date": str(datetime.today().date())
        }}

        # Create project draft
        url = reverse("project-create", kwargs={"country_id": self.country_id})
        response = self.test_user_client.post(url, self.project_data, format="json")
        self.assertEqual(response.status_code, 201, response.json())

        self.project_id = response.json().get("id")

        # Publish
        url = reverse("project-publish", kwargs={"project_id": self.project_id, "country_id": self.country_id})
        response = self.test_user_client.put(url, self.project_data, format="json")
        self.assertEqual(response.status_code, 200)
