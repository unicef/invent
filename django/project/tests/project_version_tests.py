import copy
from datetime import datetime, timedelta

from rest_framework.reverse import reverse
from project.tests.setup import SetupTests
from project.models import ProjectVersion, Project


class MockRequest:
    user = None
    GET = {}
    COOKIES = {}


class ProjectVersionTests(SetupTests):

    def setUp(self):
        super().setUp()

        versions = ProjectVersion.objects.filter(project__pk=self.project_id)
        self.assertEqual(len(versions), 2)
        version = versions[0]
        project = Project.objects.get(id=self.project_id)

        self.assertEqual(version.data, project.draft)
        self.assertEqual(version.name, project.name)
        self.assertEqual(version.version, 1)
        self.assertEqual(version.user, self.userprofile)

    def test_project_versioning(self):
        url = reverse("project-publish", kwargs={"project_id": self.project_id,
                                                 "country_office_id": self.country_office.id})
        versions = list(ProjectVersion.objects.filter(project__pk=self.project_id))
        self.assertEqual(len(versions), 2)

        version = versions[-1]
        project = Project.objects.get(id=self.project_id)

        self.assertEqual(version.data, project.data)
        self.assertEqual(version.name, project.name)
        self.assertEqual(version.version, 2)
        self.assertEqual(version.user, self.userprofile)

        # publish again with same data
        response = self.test_user_client.put(url, self.project_data, format="json")
        self.assertEqual(response.status_code, 200)

        versions = ProjectVersion.objects.filter(project__pk=self.project_id)
        self.assertEqual(len(versions), 2)
        updated_data = copy.deepcopy(self.project_data)
        updated_data['project']['name'] = 'Updated_project_name'

        # publish again with new data
        response = self.test_user_client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, 200)

        versions = ProjectVersion.objects.filter(project__pk=self.project_id)
        self.assertEqual(len(versions), 3)
        version_1 = versions.filter(version=2)[0]
        version_2 = versions.filter(version=3)[0]
        self.assertEqual(version_1.data, project.data)
        self.assertEqual(version_1.name, project.name)
        project.refresh_from_db()
        self.assertEqual(version_2.data, project.data)
        self.assertEqual(version_2.name, project.name)
        self.assertNotEqual(version_1.data, version_2.data)

    def test_project_versions_history(self):
        new_data = copy.deepcopy(self.project_data)
        new_data['project']['name'] = new_data['project']['name'] + ' changed'
        new_data['project']['contact_name'] = new_data['project']['contact_name'] + ' changed'
        new_data['project']['health_focus_areas'] = [2, 3]
        new_data['project']['start_date'] = str(datetime.today().date() + timedelta(days=1))
        new_data['project']['links'] = [dict(link_type=0, link_url="https://website.com")]
        del new_data['project']['result_area']
        del new_data['project']['end_date']

        publish_url = reverse("project-publish", kwargs={"project_id": self.project_id,
                                                         "country_office_id": self.country_office.id})
        response = self.test_user_client.put(publish_url, new_data, format="json")
        self.assertEqual(response.status_code, 200)

        url = reverse("project-versions-retrieve", kwargs={"pk": self.project_id})
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)

        last_version = response.json()[-1]
        changes = last_version['changes']

        name_change = [ch for ch in changes if ch['field'] == 'name'][0]
        self.assertEqual(name_change['added'], new_data['project']['name'])
        self.assertEqual(name_change['removed'], self.project_data['project']['name'])

        contact_name_change = [ch for ch in changes if ch['field'] == 'contact_name'][0]
        self.assertEqual(contact_name_change['added'], new_data['project']['contact_name'])
        self.assertEqual(contact_name_change['removed'], self.project_data['project']['contact_name'])

        hfa_change = [ch for ch in changes if ch['field'] == 'health_focus_areas'][0]
        self.assertEqual(hfa_change['added'],
                         list(set(new_data['project']['health_focus_areas']) -
                              set(self.project_data['project']['health_focus_areas'])))
        self.assertEqual(hfa_change['removed'],
                         list(set(self.project_data['project']['health_focus_areas']) -
                              set(new_data['project']['health_focus_areas'])))

        start_date_change = [ch for ch in changes if ch['field'] == 'start_date'][0]
        self.assertEqual(start_date_change['added'], new_data['project']['start_date'])
        self.assertEqual(start_date_change['removed'], self.project_data['project']['start_date'])

        end_date_change = [ch for ch in changes if ch['field'] == 'end_date'][0]
        self.assertIsNone(end_date_change['added'])
        self.assertEqual(end_date_change['removed'], self.project_data['project']['end_date'])

        result_area_change = [ch for ch in changes if ch['field'] == 'result_area'][0]
        self.assertIsNone(result_area_change['added'])
        self.assertEqual(result_area_change['removed'], self.project_data['project']['result_area'])

        links_change = [ch for ch in changes if ch['field'] == 'links'][0]
        self.assertIsNone(links_change['added'])
        self.assertIsNone(links_change['removed'])
        self.assertTrue(links_change['special'])

        new_data['project']['result_area'] = 1
        response = self.test_user_client.put(publish_url, new_data, format="json")
        self.assertEqual(response.status_code, 200)

        url = reverse("project-versions-retrieve", kwargs={"pk": self.project_id})
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)

        last_version = response.json()[-1]
        changes = last_version['changes']

        result_area_change = [ch for ch in changes if ch['field'] == 'result_area'][0]
        self.assertEqual(result_area_change['added'], new_data['project']['result_area'])
        self.assertIsNone(result_area_change['removed'])
        self.assertFalse(result_area_change['special'])
