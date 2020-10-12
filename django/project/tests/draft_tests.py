import copy

from django.urls import reverse

from country.models import CountryOffice, Country
from project.models import Project, HealthFocusArea, HealthCategory

from project.tests.setup import SetupTests


class ProjectDraftTests(SetupTests):
    def setUp(self):
        # Published without draft in SetupsTests
        super(ProjectDraftTests, self).setUp()

        # Draft
        self.project_draft_data, *args = self.create_test_data(name='Draft Proj 1')

        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, self.project_draft_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.project_draft_id = response.json().get("id")

        # Published
        url = reverse("project-publish", kwargs={"project_id": self.project_draft_id,
                                                 "country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_data)
        data['project'].update(name='Proj 1')
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.project_pub_id = response.json().get("id")
        # Draft without published
        self.project_draft_data, *args = self.create_test_data(name='Draft Proj 2')

        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, self.project_draft_data, format="json")
        self.project_draft_id = response.json().get("id")

    def test_create_new_draft_project_basic_data(self):
        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_draft_data)
        data['project'].update(name='Draft Proj 3', implementation_overview="Test overview")
        response = self.test_user_client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['draft']['name'], 'Draft Proj 3')
        self.assertEqual(response.json()['draft']['implementation_overview'], 'Test overview')
        self.assertEqual(int(response.json()['draft']['organisation']), self.org.id)
        self.assertEqual(int(response.json()['draft']['country']), self.country_id)
        self.assertEqual(response.json()['published'], {})
        self.assertFalse(response.json()['public_id'])

    def test_create_new_draft_name_is_not_unique(self):
        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, self.project_draft_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(self.project_draft_id, response.json().get("id"))
        self.assertEqual(Project.objects.filter(name='Draft Proj 2').count(), 2)

    def test_create_new_project_bad_data(self):
        url = reverse("project-publish", kwargs={"project_id": self.project_draft_id,
                                                 "country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_data)
        data.update(name="")
        data.update(organisation="")
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_retrieve_published_project_with_draft(self):
        url = reverse("project-retrieve", kwargs={"pk": self.project_pub_id})
        response = self.test_user_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['draft']['name'], 'Proj 1')
        self.assertEqual(response.json()['published']['name'], 'Proj 1')
        self.assertTrue(response.json()['public_id'])

    def test_retrieve_draft_only(self):
        url = reverse("project-retrieve", kwargs={"pk": self.project_draft_id})
        response = self.test_user_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['draft']['name'], 'Draft Proj 2')
        self.assertEqual(response.json()['published'], {})
        self.assertFalse(response.json()['public_id'])

    def test_update_draft_project(self):
        url = reverse("project-draft", kwargs={"project_id": self.project_draft_id,
                                               "country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_draft_data)
        data['project'].update(name="TestProject98")
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_project_draft_merged_list(self):
        url = reverse("project-list", kwargs={'list_name': 'member-of'})
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertTrue("id" in response.json()[0])
        self.assertTrue(response.json()[0]["draft"])
        self.assertTrue(response.json()[0]["published"])
        self.assertTrue(response.json()[0]['public_id'])
        self.assertTrue("id" in response.json()[1])
        self.assertTrue(response.json()[1]["draft"])
        self.assertTrue(response.json()[1]["published"])
        self.assertTrue(response.json()[1]['public_id'])
        self.assertTrue("id" in response.json()[2])
        self.assertTrue(response.json()[2]["draft"])
        self.assertFalse(response.json()[2]["published"])
        self.assertFalse(response.json()[2]['public_id'])

    def test_draft_equal_to_publish_after_publish(self):
        url = reverse("project-retrieve", kwargs={"pk": self.project_draft_id})
        response = self.test_user_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['draft']['name'], 'Draft Proj 2')
        self.assertNotEqual(response.json()['draft'], response.json()['published'])

        url = reverse("project-publish", kwargs={"project_id": self.project_draft_id,
                                                 "country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_data)
        data['project'].update(name='Proj 2')
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['draft']['name'], 'Proj 2')
        self.assertEqual(response.json()['draft'], response.json()['published'])

    def test_healthcategory_str(self):
        hc = HealthCategory.objects.all().first()
        self.assertEqual(str(hc), 'Adolescent and Youth Health')

    def test_healthfocusarea_str(self):
        hfa = HealthFocusArea.objects.all().first()
        self.assertEqual(str(hfa), '[Adolescent and Youth Health] Adolescents and communicable diseases')

    def test_make_version_for_draft(self):
        url = reverse("make-version", kwargs={"project_id": self.project_draft_id})
        response = self.test_user_client.post(url, format="json")
        self.assertEqual(response.status_code, 406)

    def test_project_create_can_send_blank_fields_in(self):
        # add one new project where health_focus_areas is empty
        project_data = copy.copy(self.project_data)
        project_data['project']['name'] = "Test Project8"
        project_data['project']['health_focus_areas'] = []
        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, project_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("hsc_challenges", response.json()['draft'])

    def test_published_country_office_co_does_not_exist(self):
        url = reverse("project-publish", kwargs={"project_id": self.project_pub_id,
                                                 "country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_data)
        data['project'].update(name='unique', country_office=999)
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'project': {'country_office': ['Country office does not exist.']}})

    def test_published_country_office_cannot_change(self):
        url = reverse("project-publish", kwargs={"project_id": self.project_pub_id,
                                                 "country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_data)

        new_country_office = CountryOffice.objects.create(
            name='Test Country Office 2',
            region=Country.UNICEF_REGIONS[0][0],
            country=self.country
        )

        data['project'].update(name='unique', country_office=new_country_office.id)
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'project': {'country_office': ['Country office cannot be altered on published projects.']}})

    def test_draft_country_office_can_change(self):
        url = reverse("project-draft", kwargs={"project_id": self.project_draft_id,
                                               "country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_draft_data)

        new_country_office = CountryOffice.objects.create(
            name='Test Country Office 2',
            region=Country.UNICEF_REGIONS[0][0],
            country=self.country
        )
        data['project'].update(country_office=new_country_office.id)
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['draft']["country"], self.country.id)
        self.assertEqual(response.json()['draft']["country_office"], new_country_office.id)

    def test_published_country_office_cannot_change_even_in_draft(self):
        url = reverse("project-draft", kwargs={"project_id": self.project_pub_id,
                                               "country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_data)

        new_country_office = CountryOffice.objects.create(
            name='Test Country Office 2',
            region=Country.UNICEF_REGIONS[0][0],
            country=self.country
        )

        data['project'].update(country_office=new_country_office.id)
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'project': {'country_office': ['Country office cannot be altered on published projects.']}})
