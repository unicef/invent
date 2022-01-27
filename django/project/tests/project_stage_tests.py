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

        stages = Stage.objects.all()
        # add stages
        stages = [
            {
                'id': stages[0].id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note'
            },
            {
                'id': stages[1].id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note'
            },
            {
                'id': stages[2].id,
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

    def test_current_phase_discontinued(self):
        now = timezone.now()
        data = copy.deepcopy(self.project_data)
        stage_1 = Stage.objects.all()[0]
        stage_discontinued = Stage.objects.get(name='Discontinued')
        # add stages
        data['project']['stages'] = [
            {
                'id': stage_1.id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note'
            },
            {
                'id': stage_discontinued.id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note'
            }
        ]

        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']['current_phase'], stage_discontinued.id)

    def test_current_phase_one_before_discontinued(self):
        now = timezone.now()
        data = copy.deepcopy(self.project_data)
        stage_1 = Stage.objects.all()[0]
        discontinued_id = Stage.objects.get(name='Discontinued').id
        all_stages = list(Stage.objects.order_by('order').values_list('id', flat=True))
        one_before_discontinued_id = all_stages[all_stages.index(discontinued_id) - 1]
        # add stages
        data['project']['stages'] = [
            {
                'id': stage_1.id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note'
            },
            {
                'id': one_before_discontinued_id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note'
            }
        ]

        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']['current_phase'], one_before_discontinued_id)

    def test_current_phase_normal_case(self):
        now = timezone.now()
        data = copy.deepcopy(self.project_data)
        stages = Stage.objects.order_by('order')
        # add stages
        data['project']['stages'] = [
            {
                'id': stages[0].id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note'
            },
            {
                'id': stages[1].id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note'
            }
        ]

        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']['current_phase'], stages[2].id)

    def test_current_phase_no_phase_selected(self):
        data = copy.deepcopy(self.project_data)
        stage_1 = Stage.objects.order_by('order').first()
        data['project']['stages'] = []

        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']['current_phase'], stage_1.id)

    def test_current_phase_is_last_phase(self):
        now = timezone.now()
        data = copy.deepcopy(self.project_data)
        stages = Stage.objects.order_by('order')
        data['project']['stages'] = [
            {
                'id': stages[0].id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note'
            },
            {
                'id': stages.last().id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note'
            }
        ]

        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']['current_phase'], stages.last().id)
