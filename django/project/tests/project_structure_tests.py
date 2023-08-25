from project.views import ProjectPublicViewSet
from django.test import TestCase


class ProjectPublicViewSetTestCase(TestCase):

    def setUp(self):
        self.viewset = ProjectPublicViewSet()

    def test_get_updated_stages(self):
        stages = [
            {'id': 1, 'name': 'Stage 1', 'tooltip': 'Tooltip 1', 'order': 1, 'link': 'null',
                'completion_marks_an_initiative_as_inactive': True},
            {'id': 2, 'name': 'Stage 2', 'tooltip': 'Tooltip 2', 'order': 2, 'link': 'null',
                'completion_marks_an_initiative_as_inactive': False},
            {'id': 3, 'name': 'Stage 3', 'tooltip': 'Tooltip 3', 'order': 3, 'link': 'null',
                'completion_marks_an_initiative_as_inactive': False},
        ]
        with self.assertNumQueries(1):
            self.assertEqual(self.viewset.get_updated_stages(), stages)

    def test_project_structure(self):
        response = self.viewset.project_structure(None)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

    def test_project_structure_phases_stages(self):
        response = self.viewset.project_structure(None)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertIn('phases_stages', response.data)
