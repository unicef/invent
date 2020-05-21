from copy import copy

from django.urls import reverse
from rest_framework import status

from django.core import mail
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from user.models import Organisation, UserProfile
from project.models import Project

from project.tests.setup import SetupTests
from user.tests import UserTests


class PermissionTests(SetupTests):
    def test_team_member_can_update_project_groups(self):
        user_2 = User.objects.create_superuser(username='test_2', email='test2@test.test', password='a')
        user_2_profile = UserProfile.objects.create(user=user_2, language='fr')

        url = reverse("project-groups", kwargs={"pk": self.project_id})

        user_profile_id = UserProfile.objects.first().id
        groups = {
            "team": [user_profile_id, user_2_profile.id],
            "viewers": [user_profile_id]
        }
        response = self.test_user_client.put(url, groups, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['team'], [user_profile_id, user_2_profile.id])
        self.assertEqual(response.json()['viewers'], [user_profile_id])

        self.assertEqual(len(mail.outbox), 3)

        first_en = '<meta http-equiv="content-language" content="en">' in mail.outbox[-2].message().as_string()
        en_index = -2 if first_en else -1
        fr_index = -1 if first_en else -2

        outgoing_en_email = mail.outbox[en_index].message()
        outgoing_en_email_text = outgoing_en_email.as_string()
        self.assertEqual(mail.outbox[en_index].subject,
                         "You have been added to a project in the T4D & Innovation Inventory Portal")
        self.assertIn('<meta http-equiv="content-language" content="en">', outgoing_en_email_text)
        self.assertNotIn('{{', outgoing_en_email_text)

        outgoing_fr_email_text = mail.outbox[fr_index].message().as_string()
        self.assertIn('<meta http-equiv="content-language" content="fr">', outgoing_fr_email_text)
        self.assertNotIn('{{', outgoing_fr_email_text)

    def test_team_viewer_cannot_update_project_groups(self):
        url = reverse("project-groups", kwargs={"pk": self.project_id})
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        owner_id = response.json()['team'][0]

        # Create a test user with profile.
        url = reverse("rest_register")
        data = {
            "email": "test_user2@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

        UserTests.create_profile_for_user(response)

        # Log in the user.
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data)
        test_user_key = response.json().get("token")
        test_user_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(test_user_key), format="json")
        user_profile_id = response.json().get('user_profile_id')

        # update profile.
        org = Organisation.objects.create(name="org2")
        url = reverse("userprofile-detail", kwargs={"pk": user_profile_id})
        data = {
            "name": "Test Name 2",
            "organisation": org.id,
            "country": self.country_id}
        response = test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        user_profile_id = response.json()['id']

        url = reverse("project-groups", kwargs={"pk": self.project_id})

        groups = {
            "team": [owner_id],
            "viewers": [user_profile_id]
        }
        response = self.test_user_client.put(url, groups, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['team'], [owner_id])
        self.assertEqual(response.json()['viewers'], [user_profile_id])

        # try to update it with the viewer
        response = test_user_client.put(url, groups)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'You do not have permission to perform this action.')

    def test_authenticated_users_can_list_project_groups(self):
        # Create a test user with profile.
        url = reverse("rest_register")
        data = {
            "email": "test_user2@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data, format="json")

        # Log in the user.
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data, format="json")
        test_user_key = response.json().get("token")
        test_user_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(test_user_key), format="json")
        user_profile_id = response.json().get('user_profile_id')

        # Create profile.
        org = Organisation.objects.create(name="org2")
        url = reverse("userprofile-detail", kwargs={"pk": user_profile_id})
        data = {
            "name": "Test Name 2",
            "organisation": org.id,
            "country": self.country_id}
        response = test_user_client.put(url, data, format="json")
        user_profile_id = response.json()['id']

        url = reverse("project-groups", kwargs={"pk": self.project_id})

        response = self.test_user_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("team" in response.json())
        self.assertTrue("viewers" in response.json())
        self.assertTrue(user_profile_id not in response.json()['team'])
        self.assertTrue(user_profile_id not in response.json()['viewers'])

    def test_not_authenticated_cannot_list_project_groups(self):
        test_user_client = APIClient(format="json")

        url = reverse("project-groups", kwargs={"pk": self.project_id})

        response = test_user_client.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')

    def test_retrieve_project_anonym_user(self):
        url = reverse("project-retrieve", kwargs={"pk": self.project_id})
        anon_client = APIClient(format="json")
        response = anon_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published'].get("name"), "Test Project1")
        self.assertEqual(response.json()['published'].get("platforms"),
                         self.project_data['project']['platforms'])

        # filtering checks
        for key in Project.FIELDS_FOR_MEMBERS_ONLY + Project.FIELDS_FOR_LOGGED_IN:
            self.assertNotIn(key, response.json())

    def test_retrieve_project_non_member_user(self):
        # Create a test user with profile.
        url = reverse("rest_register")
        data = {
            "email": "test_user2@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

        UserTests.create_profile_for_user(response)

        # Log in the user.
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data, format="json")
        test_user_key = response.json().get("token")
        test_user_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(test_user_key), format="json")
        user_profile_id = response.json().get('user_profile_id')

        # update profile.
        org = Organisation.objects.create(name="org2")
        url = reverse("userprofile-detail", kwargs={"pk": user_profile_id})
        data = {
            "name": "Test Name 2",
            "organisation": org.id,
            "country": "test_country"}
        test_user_client.put(url, data, format="json")

        url = reverse("project-retrieve", kwargs={"pk": self.project_id})
        response = test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published'].get("name"), "Test Project1")
        self.assertEqual(response.json()['published'].get("platforms"),
                         self.project_data['project']['platforms'])

        # filtering checks
        for key in Project.FIELDS_FOR_MEMBERS_ONLY:
            self.assertNotIn(key, response.json())

    def test_non_member_doesnt_see_private_answers(self):
        data = copy(self.project_data)
        data['project'].update({"name": "Test private"})

        # Create project draft
        url = reverse("project-create", kwargs={"country_office_id": self.country_office.id})
        response = self.test_user_client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201, response.json())

        project_id = response.json().get("id")

        # Publish
        url = reverse("project-publish", kwargs={"project_id": project_id,
                                                 "country_office_id": self.country_office.id})
        response = self.test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)

        # Manually add answers since we don't want to go through the standard process
        project = Project.objects.get(id=project_id)
        project.data.update({"country_custom_answers": {1: ["1"], 2: ["2"]}})
        project.data.update({"country_custom_answers_private": {3: ["3"], 4: ["4"]}})
        project.save()

        # Member can see private fields
        url = reverse("project-retrieve", kwargs={"pk": project_id})
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {'1': ['1'], '2': ['2']})
        self.assertEqual(response.json()['published']['country_custom_answers_private'],
                         {'3': ['3'], '4': ['4']})

        # Create a test user with profile.
        url = reverse("rest_register")
        data = {
            "email": "test_user2@gmail.com",
            "password1": "123456hetNYOLC",
            "password2": "123456hetNYOLC"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

        UserTests.create_profile_for_user(response)

        # Log in the user.
        url = reverse("api_token_auth")
        data = {
            "username": "test_user2@gmail.com",
            "password": "123456hetNYOLC"}
        response = self.client.post(url, data, format="json")
        test_user_key = response.json().get("token")
        test_user_client = APIClient(HTTP_AUTHORIZATION="Token {}".format(test_user_key), format="json")
        user_profile_id = response.json().get('user_profile_id')

        # update profile.
        org = Organisation.objects.create(name="org2")
        url = reverse("userprofile-detail", kwargs={"pk": user_profile_id})
        data = {
            "name": "Test Name 2",
            "organisation": org.id,
            "country": "test_country"}
        response = test_user_client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())

        # Non member can only see the public answers
        url = reverse("project-retrieve", kwargs={"pk": project_id})
        response = test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['published']['country_custom_answers'], {'1': ['1'], '2': ['2']})
        self.assertFalse('country_custom_answers_private' in response.json()['published'])

    def test_members_receive_last_version_info(self):
        url = reverse("project-retrieve", kwargs={"pk": self.project_id})
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("last_version", response.json())

        url = reverse("make-version", kwargs={"project_id": self.project_id})
        self.test_user_client.post(url, format="json")
        url = reverse("get-coverage-versions", kwargs={"project_id": self.project_id})
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        url = reverse("project-retrieve", kwargs={"pk": self.project_id})
        response = self.test_user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("last_version", response.json()['published'])

    def test_project_structure_export(self):
        url = reverse("get-project-structure-export")
        response = self.test_user_client.get(url)

        self.assertEqual(len(response.data['technology_platforms']), 48)
        self.assertEqual(len(response.data['digital_strategies']), 28)
