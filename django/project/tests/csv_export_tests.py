from copy import copy

from rest_framework.reverse import reverse

from country.models import CountryCustomQuestion, DonorCustomQuestion
from project.models import Project
from project.tests.setup import SetupTests


class CSVExportTests(SetupTests):
    def test_csv_export_failed(self):
        url = reverse("csv-export")
        response = self.test_user_client.post(url, {"ids": [1, 2]}, format="json")
        self.assertEqual(response.status_code, 404)

    def test_csv_export_success(self):
        url = reverse("csv-export")
        response = self.test_user_client.post(url, {"ids": [1, 2, Project.objects.get().id]}, format="json")
        self.assertEqual(response.status_code, 200)
        headers = dict(response.items())
        self.assertEqual(headers['Content-Type'], 'text/csv')
        self.assertEqual(headers['Content-Disposition'], 'attachment; filename="csv.csv"')
        self.assertContains(response, "Test Project1")
        self.assertContains(response, "a@a.com")
        self.assertContains(response, "National Level Deployment: [Clients: 20000, Health Workers: 0, Facilities: 0]")
        self.assertContains(response, "District: dist1 [Clients: 20, Health Workers: 5, Facilities: 4], "
                                      "District: dist2 [Clients: 10, Health Workers: 2, Facilities: 8]")
        self.assertContains(response, "District: ward1 [Clients: 209, Health Workers: 59, Facilities: 49], "
                                      "District: ward2 [Clients: 109, Health Workers: 29, Facilities: 89]")
        self.assertContains(response, "Donor1, Donor2")

    def test_csv_export_success_without_coverage(self):
        url = reverse("csv-export")
        p = Project.objects.get()
        p.data.pop('coverage')
        p.data.pop('coverage_second_level')
        p.data.pop('national_level_deployment')
        p.save()
        response = self.test_user_client.post(url, {"ids": [1, 2, Project.objects.get().id]}, format="json")
        self.assertEqual(response.status_code, 200)
        headers = dict(response.items())
        self.assertEqual(headers['Content-Type'], 'text/csv')
        self.assertEqual(headers['Content-Disposition'], 'attachment; filename="csv.csv"')
        self.assertContains(response, "Test Project1")
        self.assertContains(response, "a@a.com")
        self.assertNotContains(response, "National Level Deployment: [Clients: 20000, Health Workers: 0, "
                                         "Facilities: 0]")
        self.assertNotContains(response, "District: dist1 [Clients: 20, Health Workers: 5, Facilities: 4], "
                                         "District: dist2 [Clients: 10, Health Workers: 2, Facilities: 8]")
        self.assertNotContains(response, "District: ward1 [Clients: 209, Health Workers: 59, Facilities: 49], "
                                         "District: ward2 [Clients: 109, Health Workers: 29, Facilities: 89]")

    def test_csv_country_answers_export(self):
        q1 = CountryCustomQuestion.objects.create(question="Country Question", country_id=self.country_id)
        q2 = CountryCustomQuestion.objects.create(question="Country Private Question", country_id=self.country_id,
                                                  private=True)
        CountryCustomQuestion.objects.create(question="Country Question With No Answer", country_id=self.country_id)
        url = reverse("project-publish",
                      kwargs={
                          "country_id": self.country_id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q1.id, answer=["Country Answer 1"]),
                                                dict(question_id=q2.id, answer=["Country Private Answer 1"])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {str(q1.id): ['Country Answer 1']})
        self.assertEqual(response.json()['published']['country_custom_answers_private'],
                         {str(q2.id): ['Country Private Answer 1']})

        self.country.admins.add(self.user_profile_id)
        url = reverse("csv-export")
        response = self.test_user_client.post(url, {"ids": [Project.objects.get().id], "country": self.country_id},
                                              format="json")
        self.assertContains(response, "Country Question")
        self.assertContains(response, "Country Private Question")
        self.assertContains(response, "Country Question With No Answer")
        self.assertContains(response, "Country Answer 1")
        self.assertContains(response, "Country Private Answer 1")

    def test_csv_donor_answers_export(self):
        q1 = DonorCustomQuestion.objects.create(question="Donor Question", donor_id=self.d1.id)
        q2 = DonorCustomQuestion.objects.create(question="Donor Private Question", donor_id=self.d1.id, private=True)
        DonorCustomQuestion.objects.create(question="Donor Question With No Answer", donor_id=self.d1.id)

        url = reverse("project-publish",
                      kwargs={
                          "country_id": self.country_id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=q1.id, answer=["Donor Answer 1"]),
                                                                dict(question_id=q2.id,
                                                                     answer=["Donor Private Answer 1"])]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['donor_custom_answers'],
                         {str(self.d1.id): {str(q1.id): ['Donor Answer 1']}})
        self.assertEqual(response.json()['published']['donor_custom_answers_private'],
                         {str(self.d1.id): {str(q2.id): ['Donor Private Answer 1']}})

        self.d1.admins.add(self.user_profile_id)
        url = reverse("csv-export")

        response = self.test_user_client.post(url, {"ids": [Project.objects.get().id], "donor": 999},
                                              format="json")
        self.assertNotContains(response, "Donor Question")
        self.assertNotContains(response, "Donor Private Question")

        response = self.test_user_client.post(url, {"ids": [Project.objects.get().id], "donor": self.d1.id},
                                              format="json")
        self.assertContains(response, "Donor Question")
        self.assertContains(response, "Donor Private Question")
        self.assertContains(response, "Donor Question With No Answer")
        self.assertContains(response, "Donor Answer 1")
        self.assertContains(response, "Donor Private Answer 1")
