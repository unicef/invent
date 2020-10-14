from copy import copy

from rest_framework.reverse import reverse

from country.models import CountryCustomQuestion, DonorCustomQuestion
from project.models import Project
from project.tests.setup import SetupTests


class CustomFieldTests(SetupTests):

    def test_country_answer_wrong_country(self):
        url = reverse("project-create",
                      kwargs={
                          "country_office_id": 999,
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=1, answer=["lol1"])]})

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'details': 'No such country office'})

    def test_country_answer_wrong_country_and_project(self):
        url = reverse("project-draft",
                      kwargs={
                          "country_office_id": 999,
                          "project_id": 999
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=1, answer=["lol1"])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'details': 'No such project'})

    def test_country_answers_are_ignored_if_no_questions(self):
        url = reverse("project-create",
                      kwargs={
                          "country_office_id": self.country_office.id
                      })
        data = copy(self.project_data)
        # will be ignored even if the question ID is invalid
        data.update({"country_custom_answers": [dict(question_id='a', answer=["lol1"])]})

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.json())
        self.assertFalse('country_custom_answers' in response.json())

    def test_country_answer_wrong_question_id(self):
        CountryCustomQuestion.objects.create(question="What up?", country_id=self.country_id)
        url = reverse("project-create",
                      kwargs={
                          "country_office_id": self.country_office.id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id='a', answer=["lol1"])]})

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], [{'question_id': ['A valid integer is required.']}])

        data.update({"country_custom_answers": [dict(question_id=999, answer=["lol1"])]})

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'],
                         [{'question_id': ['This question_id does not exist.']}])

    def test_country_answer_wrong_all_required(self):
        CountryCustomQuestion.objects.create(question="What up?", country_id=self.country_id)
        url = reverse("project-create",
                      kwargs={
                          "country_office_id": self.country_office.id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict()]})

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], [{'question_id': ['This field is required.'],
                                                                      'answer': ['This field is required.']}])

        url = reverse("project-draft",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], [{'question_id': ['This field is required.'],
                                                                      'answer': ['This field is required.']}])

        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], [{'question_id': ['This field is required.'],
                                                                      'answer': ['This field is required.']}])

    def test_country_answer_for_draft(self):
        q = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id)
        url = reverse("project-draft",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q.id, answer=["lol1"])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['draft']['country_custom_answers'], {str(q.id): ['lol1']})

        project = Project.objects.last()
        self.assertEqual(project.draft['country_custom_answers'], {str(q.id): ['lol1']})
        self.assertTrue('country_custom_answers' not in project.data)

    def test_country_answer_for_published(self):
        q = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q.id, answer=["lol1"])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {str(q.id): ['lol1']})
        self.assertEqual(response.json()['draft']['country_custom_answers'], {str(q.id): ['lol1']})

        project = Project.objects.last()
        self.assertEqual(project.data['country_custom_answers'], {str(q.id): ['lol1']})
        self.assertEqual(project.draft['country_custom_answers'], {str(q.id): ['lol1']})

    def test_country_answer_for_published_is_required(self):
        q1 = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id, required=True)
        q2 = CountryCustomQuestion.objects.create(question="test2", country_id=self.country_id, required=True)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        # answer key present but empty
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q1.id, answer=[])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], [{'answer': ['This field is required.']}])

        # answer key not present
        data.update({"country_custom_answers": [dict(question_id=q1.id)]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], [{'answer': ['This field is required.']}])

        # answer one is present, but answer 2 is missing
        data.update({"country_custom_answers": [dict(question_id=q1.id, answer=["answer1"])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], {str(q2.id): ['This field is required']})

        # country custom answers are missing
        data.pop('country_custom_answers', None)

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Country answers are missing')

        url = reverse("project-create",
                      kwargs={
                          "country_office_id": self.country_office.id,
                      })

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Country answers are missing')

        url = reverse("project-draft",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Country answers are missing')

    def test_country_answer_numeric_validation(self):
        q = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id,
                                                 type=CountryCustomQuestion.NUMBER)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q.id, answer=["123a"])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], [{'answer': ['This field must be numeric.']}])

        data.update({"country_custom_answers": [dict(question_id=q.id, answer=["123"])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {str(q.id): ['123']})

    def test_country_answer_length_validation(self):
        q1 = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id,
                                                  type=CountryCustomQuestion.TEXT)
        q2 = CountryCustomQuestion.objects.create(question="test multi", country_id=self.country_id,
                                                  type=CountryCustomQuestion.MULTI)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q1.id, answer=['1', '2'])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], [{'answer': ['There must be 1 answer only.']}])

        data.update({"country_custom_answers": [dict(question_id=q2.id, answer=['1', '2'])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {str(q2.id): ['1', '2']})

    def test_country_answer_update_existing_answer(self):
        q = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q.id, answer=["lol1"], draft=False)]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {str(q.id): ['lol1']})

        data.update({"country_custom_answers": [dict(question_id=q.id, answer=["lol2"], draft=False)]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {str(q.id): ['lol2']})

        project = Project.objects.last()
        self.assertEqual(project.data['country_custom_answers'], {str(q.id): ['lol2']})
        self.assertEqual(project.draft['country_custom_answers'], {str(q.id): ['lol2']})

    def test_country_answer_new_required_question(self):
        q1 = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q1.id, answer=["lol1"])]})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {str(q1.id): ['lol1']})

        q2 = CountryCustomQuestion.objects.create(question="test2", country_id=self.country_id, required=True)

        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['country_custom_answers'], {str(q2.id): ['This field is required']})

        data.update({"country_custom_answers": [dict(question_id=q1.id, answer=["lol1"]), dict(question_id=q2.id,
                                                                                               answer=["lol2"])]})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'],
                         {str(q1.id): ['lol1'], str(q2.id): ['lol2']})

    def test_country_private_answers_are_saved_separately(self):
        q1 = CountryCustomQuestion.objects.create(question="test private", country_id=self.country_id, private=True)
        q2 = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id)
        q3 = CountryCustomQuestion.objects.create(question="test2 private", country_id=self.country_id, private=True)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"country_custom_answers": [dict(question_id=q1.id, answer=["private answer 1"]),
                                                dict(question_id=q2.id, answer=["public answer"]),
                                                dict(question_id=q3.id, answer=["private answer 2"])]})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {str(q2.id): ['public answer']})
        self.assertEqual(response.json()['published']['country_custom_answers_private'],
                         {str(q1.id): ['private answer 1'], str(q3.id): ['private answer 2']})

    def test_reorder_country_questions_unsuccessful(self):
        q = CountryCustomQuestion.objects.create(question="test3", country_id=self.country_id)

        url = reverse("country-custom-questions-set-order-to", kwargs={"pk": q.id})
        response = self.test_user_client.post(url, format='json')
        self.assertEqual(response.status_code, 400)

        response = self.test_user_client.post(url, data={'to': 'a'}, format='json')
        self.assertEqual(response.status_code, 400)

        url = reverse("country-custom-questions-set-order-to", kwargs={"pk": 999})
        response = self.test_user_client.post(url, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_reorder_country_questions_success(self):
        q1 = CountryCustomQuestion.objects.create(question="test", country_id=self.country_id)
        q2 = CountryCustomQuestion.objects.create(question="test2", country_id=self.country_id)
        q3 = CountryCustomQuestion.objects.create(question="test3", country_id=self.country_id)

        url = reverse("country-detail", kwargs={"pk": self.country_id})
        response = self.test_user_client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['country_questions']), 3)
        self.assertTrue(response.json()['country_questions'][0]['id'] <
                        response.json()['country_questions'][1]['id'] <
                        response.json()['country_questions'][2]['id'])
        self.assertTrue(response.json()['country_questions'][0]['order'] <
                        response.json()['country_questions'][1]['order'] <
                        response.json()['country_questions'][2]['order'])

        url = reverse("country-custom-questions-set-order-to", kwargs={"pk": q3.id})
        response = self.test_user_client.post(url, data={'to': str(response.json()['country_questions'][0]['order'])},
                                              format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': q3.id, 'order': 0},
                                           {'id': q1.id, 'order': 1},
                                           {'id': q2.id, 'order': 2}])

        url = reverse("country-detail", kwargs={"pk": self.country_id})
        response = self.test_user_client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['country_questions'][1]['id'] <
                        response.json()['country_questions'][2]['id'] <
                        response.json()['country_questions'][0]['id'])
        self.assertTrue(response.json()['country_questions'][0]['order'] <
                        response.json()['country_questions'][1]['order'] <
                        response.json()['country_questions'][2]['order'])

    def test_reorder_donor_questions_success(self):
        dq1 = DonorCustomQuestion.objects.create(question="test", donor_id=self.d1.id)
        dq2 = DonorCustomQuestion.objects.create(question="test2", donor_id=self.d1.id)
        dq3 = DonorCustomQuestion.objects.create(question="test3", donor_id=self.d1.id)

        url = reverse("donor-detail", kwargs={"pk": self.d1.id})
        response = self.test_user_client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['donor_questions']), 3)
        self.assertTrue(response.json()['donor_questions'][0]['id'] <
                        response.json()['donor_questions'][1]['id'] <
                        response.json()['donor_questions'][2]['id'])
        self.assertTrue(response.json()['donor_questions'][0]['order'] <
                        response.json()['donor_questions'][1]['order'] <
                        response.json()['donor_questions'][2]['order'])

        url = reverse("donor-custom-questions-set-order-to", kwargs={"pk": dq3.id})
        response = self.test_user_client.post(url, data={'to': str(response.json()['donor_questions'][0]['order'])},
                                              format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': dq3.id, 'order': 0},
                                           {'id': dq1.id, 'order': 1},
                                           {'id': dq2.id, 'order': 2}])

    def test_donor_answer_for_draft(self):
        q = DonorCustomQuestion.objects.create(question="test", donor_id=self.d1.id)
        url = reverse("project-draft",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=q.id, answer=["lol1"])]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['draft']['donor_custom_answers'], {str(self.d1.id): {str(q.id): ['lol1']}})

        project = Project.objects.last()
        self.assertEqual(project.draft['donor_custom_answers'], {str(self.d1.id): {str(q.id): ['lol1']}})
        self.assertTrue('donor_custom_answers' not in project.data)

    def test_donor_answer_for_published(self):
        q = DonorCustomQuestion.objects.create(question="test", donor_id=self.d1.id)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        data = copy(self.project_data)
        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=q.id, answer=["lol1"])]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['donor_custom_answers'], {str(self.d1.id): {str(q.id): ['lol1']}})
        self.assertEqual(response.json()['draft']['donor_custom_answers'], {str(self.d1.id): {str(q.id): ['lol1']}})

        project = Project.objects.last()
        self.assertEqual(project.data['donor_custom_answers'], {str(self.d1.id): {str(q.id): ['lol1']}})
        self.assertEqual(project.draft['donor_custom_answers'], {str(self.d1.id): {str(q.id): ['lol1']}})

    def test_donor_answer_for_all_is_required(self):
        dq1 = DonorCustomQuestion.objects.create(question="test", donor_id=self.d1.id, required=True)
        dq2 = DonorCustomQuestion.objects.create(question="test2", donor_id=self.d1.id, required=True)
        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })
        # answer key present but empty
        data = copy(self.project_data)
        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=dq1.id, answer=[])]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'answer': ['This field is required.']}]})

        # answer key not present
        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=dq1.id)]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'answer': ['This field is required.']}]})

        # answer one is present, but answer 2 is missing
        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=dq1.id, answer=["answer1"])]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): {str(dq2.id): ['This field is required']}})

        # donor custom answers are missing
        data.pop('donor_custom_answers', None)

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Donor answers are missing')

        url = reverse("project-create",
                      kwargs={
                          "country_office_id": self.country_office.id,
                      })

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Donor answers are missing')

        url = reverse("project-draft",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Donor answers are missing')

        # donor custom answer for donor one are missing
        data.update({"donor_custom_answers": {}})
        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Donor answers are missing')

        url = reverse("project-create",
                      kwargs={
                          "country_office_id": self.country_office.id,
                      })

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Donor answers are missing')

        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'], 'Donor answers are missing')

        # answer 1 and 2 are present, there is an extra non existing donor
        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=dq1.id, answer=["answer1"]),
                                                                dict(question_id=dq2.id, answer=["answer2"])],
                                              str(999): [dict(question_id=333, answer=[])]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_donor_answer_wrong_question_id(self):
        DonorCustomQuestion.objects.create(question="What up?", donor_id=self.d1.id)
        url = reverse("project-create",
                      kwargs={
                          "country_office_id": self.country_office.id
                      })
        data = copy(self.project_data)
        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id='a', answer=["lol1"])]}})

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['A valid integer is required.']}]})

        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=999, answer=["lol1"])]}})

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['This question_id does not exist.']}]})

        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['This question_id does not exist.']}]})

        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id='a', answer=["lol1"])]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['A valid integer is required.']}]})

        url = reverse("project-draft",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['A valid integer is required.']}]})

        data.update({"donor_custom_answers": {str(self.d1.id): [dict(question_id=999, answer=["lol1"])]}})

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['This question_id does not exist.']}]})

    def test_donor_answer_wrong_all_required(self):
        DonorCustomQuestion.objects.create(question="What up?", donor_id=self.d1.id)
        url = reverse("project-create",
                      kwargs={
                          "country_office_id": self.country_office.id
                      })
        data = copy(self.project_data)
        data.update({"donor_custom_answers": {str(self.d1.id): [dict()]}})

        response = self.test_user_client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['This field is required.'],
                                             'answer': ['This field is required.']}]})

        url = reverse("project-draft",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['This field is required.'],
                                             'answer': ['This field is required.']}]})

        url = reverse("project-publish",
                      kwargs={
                          "country_office_id": self.country_office.id,
                          "project_id": self.project_id
                      })

        response = self.test_user_client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['donor_custom_answers'],
                         {str(self.d1.id): [{'question_id': ['This field is required.'],
                                             'answer': ['This field is required.']}]})
