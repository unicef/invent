import copy

from rest_framework.reverse import reverse

from project.models import Project
from project.tests.setup import SetupTests


class ODKProjectTests(SetupTests):
    def test_post_draft_with_odk_stuff(self):
        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        data = copy.deepcopy(self.project_data)

        odk_etag = "59605878-6a6a-4f5f-9262-256939398333"
        odk_id = "dfdsfk-dsfsdf-sd-f-sdf-sdfafdsf"
        odk_extra_data = {"dict": {"of": "dicts"}}

        data['project'].update(dict(
            name="Test Project From ODK",
            odk_etag=odk_etag,
            odk_id=odk_id,
            odk_extra_data=odk_extra_data
        ))

        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

        project_draft_id = response.json()['id']
        project = Project.objects.get(id=project_draft_id)

        self.assertEqual(project.odk_etag, odk_etag)
        self.assertEqual(project.odk_id, odk_id)
        self.assertEqual(project.odk_extra_data, odk_extra_data)

        url = reverse("project-draft",
                      kwargs={"country_office_id": self.country_office.id, "project_id": project_draft_id})
        data['project'].update(odk_etag="59605878-6a6a-4f5f-9262-256939398334")

        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)

        project.refresh_from_db()
        self.assertIsNone(project.odk_etag)
        self.assertEqual(project.odk_id, odk_id)
        self.assertEqual(project.odk_extra_data, odk_extra_data)
