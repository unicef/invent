import copy

from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse

from project.models import Stage
from project.tests.setup import SetupTests


class ProjectStageTests(SetupTests):

    def test_project_stages(self):
        now = timezone.now()

        data = copy.deepcopy(self.project_data)

        data['project']['name'] = 'Test Project 100'
        data['project']['start_date'] = str((now - timezone.timedelta(days=10)).date())
        data['project']['end_date'] = str((now - timezone.timedelta(days=1)).date())
        data['project']['end_date_note'] = "note for end date"
        del data['project']['stages']

        # create project
        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

        project_id = response.json()['id']
        self.assertIn("end_date_note", response.json()['draft'])

        # add stage without date
        stages = [
            {
                'id': 3,
                'date': None,
                'note': None
            }
        ]
        data['project']['stages'] = stages
        url = reverse("project-draft", kwargs={"project_id": project_id,
                                               "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.json())
        self.assertEqual(response.json(), {'project': {'stages': [{'date': ['This field may not be null.']}]}})

        # add stages
        stages = [
            {
                'id': 1,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note'
            },
            {
                'id': 2,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note'
            },
            {
                'id': 3,
                'date': str((now - timezone.timedelta(days=3)).date()),
                'note': None
            }
        ]
        data['project']['stages'] = stages

        url = reverse("project-draft", kwargs={"project_id": project_id,
                                               "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        resp_data = response.json()
        self.assertIn('stages', resp_data['draft'])
        self.assertEqual(len(resp_data['draft']['stages']), 3)

        # try to publish without stages
        del data['project']['stages']
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        resp_data = response.json()
        self.assertNotIn('stages', resp_data['draft'])
        self.assertIn("end_date_note", response.json()['draft'])

        # publish with stages
        data['project']['stages'] = stages
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        resp_data = response.json()
        self.assertIn('stages', resp_data['draft'])
        self.assertEqual(len(resp_data['draft']['stages']), 3)

    def test_stage_list(self):
        Stage.objects.all().delete()

        stage_c = Stage.objects.create(name='Stage C', order='3')
        stage_a = Stage.objects.create(name='Stage A', order='2')
        stage_b = Stage.objects.create(name='Stage B', order='1')

        url = reverse("get-project-structure")
        response = self.test_user_client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        data = response.json()['stages']
        self.assertEqual(data[0]['id'], stage_b.id)
        self.assertEqual(data[1]['id'], stage_a.id)
        self.assertEqual(data[2]['id'], stage_c.id)
