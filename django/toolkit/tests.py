from math import ceil

from django.core import mail
from django.urls import reverse

from user.models import UserProfile
from .models import Toolkit
from . import tasks

from project.tests.setup import SetupTests


class ToolkitTests(SetupTests):

    def setUp(self):
        super(ToolkitTests, self).setUp()

        url = reverse("project-groups", kwargs={"pk": self.project_id})
        groups = {
            "team": [self.user_profile_id],
            "viewers": []
        }
        self.test_user_client.put(url, groups)

    def test_set_score(self):
        url = reverse("toolkit-scores", kwargs={"project_id": self.project_id})
        data = {
                "axis": 0,
                "domain": 0,
                "question": 0,
                "answer": 0,
                "value": 2
            }
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        toolkit = Toolkit.objects.get_object_or_none(project=self.project_id)
        self.assertEqual(toolkit.data[0]["domains"][0]["questions"][0]["answers"][0], 2)

    def test_set_score_fail(self):
        url = reverse("toolkit-scores", kwargs={"project_id": self.project_id})
        data = {
                "axis": 0,
                "domain": 0,
                "question": 0,
                "answer": 0,
                "value": "2s"
            }
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['value'][0], 'A valid integer is required.')

    def test_set_score_wrong_index(self):
        url = reverse("toolkit-scores", kwargs={"project_id": self.project_id})
        data = {
                "axis": 999,
                "domain": 0,
                "question": 0,
                "answer": 0,
                "value": 2
            }
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("No such answer.", response.json()["details"])

    def test_set_score_wrong_project_id(self):
        url = reverse("toolkit-scores", kwargs={"project_id": 999})
        data = {
                "axis": 0,
                "domain": 0,
                "question": 0,
                "answer": 0,
                "value": 2
            }
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("No such project.", response.json()["details"])

    def test_get_toolkit_data(self):
        url = reverse("toolkit-scores", kwargs={"project_id": self.project_id})
        data = {
                "axis": 0,
                "domain": 0,
                "question": 0,
                "answer": 0,
                "value": 2
            }
        self.test_user_client.post(url, data, format="json")
        url = reverse("toolkit-data", kwargs={"project_id": self.project_id})
        response = self.test_user_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["domains"][0]["questions"][0]["answers"][0], 2)

    def test_get_toolkit_data_wrong_project_id(self):
        url = reverse("toolkit-data", kwargs={"project_id": 999})
        response = self.test_user_client.get(url, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("No such project.", response.json()["details"])

    def test_get_toolkit_data_statistics(self):
        url = reverse("toolkit-scores", kwargs={"project_id": self.project_id})
        data = {
                "axis": 0,
                "domain": 0,
                "question": 0,
                "answer": 0,
                "value": 2
            }
        response = self.test_user_client.post(url, data, format="json")
        data = {
                "axis": 0,
                "domain": 1,
                "question": 0,
                "answer": 0,
                "value": 3
            }
        response = self.test_user_client.post(url, data, format="json")
        url = reverse("toolkit-data", kwargs={"project_id": self.project_id})
        response = self.test_user_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["domains"][0]["questions"][0]["answers"][0], 2)
        self.assertEqual(response.json()[0]["domains"][0]["domain_sum"], 2)
        self.assertEqual(ceil(response.json()[0]["domains"][0]["domain_percentage"]), 100)
        self.assertEqual(ceil(response.json()[0]["domains"][0]["domain_completion"]), 100)
        self.assertEqual(response.json()[0]["domains"][1]["questions"][0]["answers"][0], 3)
        self.assertEqual(response.json()[0]["domains"][1]["domain_sum"], 3)
        self.assertEqual(ceil(response.json()[0]["domains"][1]["domain_percentage"]), 14)
        self.assertEqual(ceil(response.json()[0]["domains"][1]["domain_completion"]), 10)
        self.assertEqual(ceil(response.json()[0]["axis_score"]), 38)
        self.assertEqual(ceil(response.json()[0]["axis_completion"]), 9)

    def test_send_daily_toolkit_digest(self):
        url = reverse("toolkit-scores", kwargs={"project_id": self.project_id})
        data = {
                "axis": 0,
                "domain": 0,
                "question": 0,
                "answer": 0,
                "value": 2
            }
        self.test_user_client.post(url, data, format="json")
        tasks.send_daily_toolkit_digest()
        self.assertEqual(mail.outbox[-1].subject, "Your Digital Health Atlas project has been updated")

        profile = UserProfile.objects.get(id=self.user_profile_id)
        self.assertEqual(profile.language, 'en')
        self.assertIn('<meta http-equiv="content-language" content="en">',
                      str(mail.outbox[-1].message()))

        # check other language
        profile.language = 'fr'
        profile.save()
        tasks.send_daily_toolkit_digest()

        self.assertIn('<meta http-equiv="content-language" content="fr">',
                      str(mail.outbox[-1].message()))
