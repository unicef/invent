import copy
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
