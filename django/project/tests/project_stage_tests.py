import copy

from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse

from project.models import Stage
from project.tests.setup import SetupTests
from django.test import TestCase
from project.views import ProjectPublicViewSet

class ProjectStageTests(SetupTests):

    def test_project_stages(self):
        now = timezone.now()

        data = copy.deepcopy(self.project_data)

        data['project']['name'] = 'Test Project 100'
        data['project']['start_date'] = str(
            (now - timezone.timedelta(days=10)).date())
        data['project']['end_date'] = str(
            (now - timezone.timedelta(days=1)).date())
        data['project']['end_date_note'] = "note for end date"
        del data['project']['stages']

        # create project
        url = reverse("project-create",
                      kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.json())

        project_id = response.json()['id']
        self.assertIn("end_date_note", response.json()['draft'])

        # add stage without date
        stages = [
            {
                'id': 3,
                'date': None,
                'note': None,
                'completion_marks_an_initiative_as_inactive': False,
            }
        ]
        data['project']['stages'] = stages
        url = reverse("project-draft", kwargs={"project_id": project_id,
                                               "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, response.json())
        self.assertEqual(response.json(), {'project': {'stages': [
                         {'date': ['This field may not be null.']}]}})

        stages = Stage.objects.all()
        # add stages
        stages = [
            {
                'id': stages[0].id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stages[1].id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stages[2].id,
                'date': str((now - timezone.timedelta(days=3)).date()),
                'note': None,
                'completion_marks_an_initiative_as_inactive': False,
            }
        ]
        data['project']['stages'] = stages

        url = reverse("project-draft", kwargs={"project_id": project_id,
                                               "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.json())
        resp_data = response.json()
        self.assertIn('stages', resp_data['draft'])
        self.assertEqual(len(resp_data['draft']['stages']), 3)

        # try to publish without stages
        del data['project']['stages']
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.json())
        resp_data = response.json()
        self.assertNotIn('stages', resp_data['draft'])
        self.assertIn("end_date_note", response.json()['draft'])

        # publish with stages
        data['project']['stages'] = stages
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.json())
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
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.json())
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
                'note': 'preparation note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stage_discontinued.id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note',
                'completion_marks_an_initiative_as_inactive': False,
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
                'note': 'preparation note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': one_before_discontinued_id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note',
                'completion_marks_an_initiative_as_inactive': True,
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
                'note': 'preparation note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stages[1].id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note',
                'completion_marks_an_initiative_as_inactive': False,
            }
        ]

        url = reverse("project-create",
                      kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']
                         ['current_phase'], stages[2].id)

    def test_current_phase_no_phase_selected(self):
        data = copy.deepcopy(self.project_data)
        stage_1 = Stage.objects.order_by('order').first()
        data['project']['stages'] = []

        url = reverse("project-create",
                      kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']['current_phase'], stage_1.id)

    def test_current_phase_is_last_phase(self):
        now = timezone.now()
        data = copy.deepcopy(self.project_data)
        stages = Stage.objects.order_by('order')
        data['project']['stages'] = [
            {
                'id': stages[0].id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stages.last().id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note',
                'completion_marks_an_initiative_as_inactive': False,
            }
        ]

        url = reverse("project-create",
                      kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']
                         ['current_phase'], stages.last().id)


class ProjectStageTests(SetupTests):

    @staticmethod
    def calc_current_phase(stages):
        all_stages = list(Stage.objects.order_by(
            "order").values_list("id", flat=True))
        if not stages:  # when no phases are selected, the current phase is the first one
            return all_stages[0]

        stage_ids = [stage["id"] for stage in stages]
        # get the completed phases of the initiative and order them
        selected_stages = Stage.objects.filter(
            id__in=stage_ids).order_by("order")
        # get the last phase from initiative's completed phases
        last_stage = selected_stages.last()

        # apply the business requirements
        if not last_stage.completion_marks_an_initiative_as_inactive:  # selected phase's checkbox unchecked
            # compute if there are already previous completed end phases (checkbox=checked)
            completed_stages = selected_stages.filter(
                completion_marks_an_initiative_as_inactive=True)
            if completed_stages:  # if there are completed end phases
                current = last_stage.id
            else:  # if there are no completed end phases
                if last_stage.id != all_stages[-1]:  # not the last in the list
                    current = all_stages[all_stages.index(
                        last_stage.id) + 1]  # get the next phase
                else:  # the last in the list
                    current = last_stage.id  # set this phase as current
        else:  # selected phase's checkbox checked
            current = last_stage.id  # set this phase as current

        return current

    def test_project_stages(self):
        now = timezone.now()

        data = copy.deepcopy(self.project_data)

        data['project']['name'] = 'Test Project 100'
        data['project']['start_date'] = str(
            (now - timezone.timedelta(days=10)).date())
        data['project']['end_date'] = str(
            (now - timezone.timedelta(days=1)).date())
        data['project']['end_date_note'] = "note for end date"
        del data['project']['stages']

        # create project
        url = reverse("project-create",
                      kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.json())

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
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, response.json())
        self.assertEqual(response.json(), {'project': {'stages': [
                         {'date': ['This field may not be null.']}]}})

        stages = Stage.objects.all()
        # add stages
        stages = [
            {
                'id': stages[0].id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stages[1].id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stages[2].id,
                'date': str((now - timezone.timedelta(days=3)).date()),
                'note': None,
                'completion_marks_an_initiative_as_inactive': False,
            }
        ]
        data['project']['stages'] = stages

        url = reverse("project-draft", kwargs={"project_id": project_id,
                                               "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.json())
        resp_data = response.json()
        self.assertIn('stages', resp_data['draft'])
        self.assertEqual(len(resp_data['draft']['stages']), 3)

        # try to publish without stages
        del data['project']['stages']
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.json())
        resp_data = response.json()
        self.assertNotIn('stages', resp_data['draft'])
        self.assertIn("end_date_note", response.json()['draft'])

        # publish with stages
        data['project']['stages'] = stages
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.json())
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
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.json())
        data = response.json()['stages']
        self.assertEqual(data[0]['id'], stage_b.id)
        self.assertEqual(data[1]['id'], stage_a.id)
        self.assertEqual(data[2]['id'], stage_c.id)

    def test_current_phase_normal_case(self):
        now = timezone.now()
        data = copy.deepcopy(self.project_data)
        stages = Stage.objects.order_by('order')
        # add stages
        data['project']['stages'] = [
            {
                'id': stages[0].id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stages[1].id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note',
                'completion_marks_an_initiative_as_inactive': False,
            }
        ]

        url = reverse("project-create",
                      kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']
                         ['current_phase'], stages[2].id)

    def test_current_phase_no_phase_selected(self):
        data = copy.deepcopy(self.project_data)
        stage_1 = Stage.objects.order_by('order').first()
        data['project']['stages'] = []

        url = reverse("project-create",
                      kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']['current_phase'], stage_1.id)

    def test_current_phase_is_last_phase(self):
        now = timezone.now()
        data = copy.deepcopy(self.project_data)
        stages = Stage.objects.order_by('order')
        data['project']['stages'] = [
            {
                'id': stages[0].id,
                'date': str((now - timezone.timedelta(days=10)).date()),
                'note': 'preparation note',
                'completion_marks_an_initiative_as_inactive': False,
            },
            {
                'id': stages.last().id,
                'date': str((now - timezone.timedelta(days=7)).date()),
                'note': 'analysis note',
                'completion_marks_an_initiative_as_inactive': False,
            }
        ]

        url = reverse("project-create",
                      kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.json()['draft']
                         ['current_phase'], stages.last().id)


class ProjectPublicViewSetTestCase(TestCase):
    def setUp(self):
        self.viewset = ProjectPublicViewSet()

    def test_get_updated_stages(self):
        stages = [
            {'id': 1, 'name': 'Stage 1', 'tooltip': 'Tooltip 1', 'order': 1,
                'completion_marks_an_initiative_as_inactive': True},
            {'id': 2, 'name': 'Stage 2', 'tooltip': 'Tooltip 2', 'order': 2,
                'completion_marks_an_initiative_as_inactive': False}
        ]
        with self.assertNumQueries(1):
            self.assertEqual(self.viewset.get_updated_stages(), stages)

    def test_project_structure(self):
        response = self.viewset.project_structure(None)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        # Add assertions for the expected structure of the response

    def setUp(self):
        self.viewset = ProjectPublicViewSet()

    def test_get_updated_stages(self):
        stages = [
            {'id': 1, 'name': 'Stage 1', 'tooltip': 'Tooltip 1', 'order': 1,
                'completion_marks_an_initiative_as_inactive': True},
            {'id': 2, 'name': 'Stage 2', 'tooltip': 'Tooltip 2', 'order': 2,
                'completion_marks_an_initiative_as_inactive': False},
            {'id': 3, 'name': 'Stage 3', 'tooltip': 'Tooltip 3', 'order': 3,
                'completion_marks_an_initiative_as_inactive': False},
        ]
        with self.assertNumQueries(1):
            self.assertEqual(self.viewset.get_updated_stages(), stages)

    def test_project_structure(self):
        response = self.viewset.project_structure(None)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        # Add assertions for the expected structure of the response

    def test_project_structure_phases_stages(self):
        response = self.viewset.project_structure(None)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertIn('phases_stages', response.data)


class StageTestCase(TestCase):
    def setUp(self):
        self.stage_data = {
            'name': 'Test Stage',
            # Set the value accordingly for your test
            'completion_marks_an_initiative_as_inactive': True
        }

    def test_completion_marks_an_initiative_as_inactive(self):
        # Create a stage
        stage = Stage.objects.create(**self.stage_data)

        # Retrieve the created stage from the database
        created_stage = Stage.objects.get(id=stage.id)

        # Assert the field value matches the expected value
        self.assertEqual(created_stage.completion_marks_an_initiative_as_inactive,
                         self.stage_data['completion_marks_an_initiative_as_inactive'])

        # Update the field value
        new_value = False  # Set the new value accordingly for your test
        created_stage.completion_marks_an_initiative_as_inactive = new_value
        created_stage.save()

        # Retrieve the updated stage from the database
        updated_stage = Stage.objects.get(id=stage.id)

        # Assert the field value has been updated
        self.assertEqual(
            updated_stage.completion_marks_an_initiative_as_inactive, new_value)
