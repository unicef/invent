from unittest import mock
from unittest.mock import _CallList

from django.contrib.auth.models import User
from django.test import override_settings
from django.utils import timezone
from freezegun import freeze_time

from country.models import Donor, DonorCustomQuestion
from project.models import Project
from project.tasks import project_still_in_draft_notification, published_projects_updated_long_ago
from project.tests.setup import SetupTests
from user.models import UserProfile


class ProjectNotificationTests(SetupTests):

    def setUp(self):
        super(ProjectNotificationTests, self).setUp()

        self.user_1 = User.objects.create(username='bh_1', email='bh+1@pulilab.com')
        self.profile_1 = UserProfile.objects.create(user=self.user_1)
        self.user_2 = User.objects.create(username='bh_2', email='bh+2@pulilab.com')
        self.profile_2 = UserProfile.objects.create(user=self.user_2)
        self.user_3 = User.objects.create(username='bh_3', email='bh+3@pulilab.com')
        self.profile_3 = UserProfile.objects.create(user=self.user_3)
        self.user_4 = User.objects.create(username='bh_4', email='bh+4@pulilab.com')
        self.profile_4 = UserProfile.objects.create(user=self.user_4)
        self.user_5 = User.objects.create(username='bh_5', email='bh+5@pulilab.com')
        self.profile_5 = UserProfile.objects.create(user=self.user_5)

        self.published_project_data = dict(
            country=self.country.id, country_office=self.country_office.id,
            organisation=self.org.id, hsc_challenges=[1, 2], platforms=[1, 2],
            capability_categories=[], capability_levels=[], capability_subcategories=[])

        self.unicef, _ = Donor.objects.get_or_create(name='UNICEF')
        self.custom_question = DonorCustomQuestion.objects.create(
            question="Stage",
            donor_id=self.unicef.id,
            options=[
                "Opportunity and Ideation", "Preparation", "Analysis and Design", "Implementation Planning",
                "Developing or Adapting Solution", "Piloting and Evidence Generation", "Package and Champion",
                "Deploying", "Scaling up", "Scale and Handover", "Under Review", "Discontinued"
            ]
        )

    @staticmethod
    def add_donor_custom_answers_to_project(project, donor_id, custom_question_id, answer):
        project.draft = {
            "donor_custom_answers": {
                donor_id: {
                    custom_question_id: answer,
                }
            }
        }
        project.save()

    @mock.patch('project.tasks.send_mail_wrapper', return_value=None)
    def test_project_still_in_draft_notification(self, send_mail_wrapper):
        now = timezone.now()

        with freeze_time(now - timezone.timedelta(days=40)):
            draft_project_1 = Project.objects.create(name='Draft project 1', public_id='')
            draft_project_1.team.add(self.profile_1)

            # make a published project without API calls
            published_project = Project.objects.create(
                name='Published project 1', data=self.published_project_data, public_id='1234')
            published_project.team.add(self.profile_1)

        with freeze_time(now - timezone.timedelta(days=32)):
            draft_project_2 = Project.objects.create(name='Draft project 2', public_id='')
            draft_project_2.team.add(self.profile_2)

        with freeze_time(now - timezone.timedelta(days=20)):
            draft_project_3 = Project.objects.create(name='Draft project 3', public_id='')
            draft_project_3.team.add(self.profile_3)

        with freeze_time(now - timezone.timedelta(days=45)):
            draft_project_4 = Project.objects.create(name='Draft project 4', public_id='')
            draft_project_4.team.add(self.profile_4)

            # draft_project_4 should be excluded because it is in "Scale and Handover" state
            self.add_donor_custom_answers_to_project(
                draft_project_4, self.unicef.id, self.custom_question.id, ['Scale and Handover'])

            draft_project_5 = Project.objects.create(name='Draft project 5', public_id='')
            draft_project_5.team.add(self.profile_5)

            # draft_project_5 should be excluded because it is in "Discontinued" state
            self.add_donor_custom_answers_to_project(
                draft_project_5, self.unicef.id, self.custom_question.id, ['Discontinued'])

        with override_settings(EMAIL_SENDING_PRODUCTION=True):
            project_still_in_draft_notification.apply()

            # task should send emails about Draft project 1 and Draft project 2
            self.assertEqual(len(send_mail_wrapper.call_args_list), 2)

            call_args_list_1 = send_mail_wrapper.call_args_list[0][1]
            self.assertEqual(call_args_list_1['subject'], 'Project has been in draft state for over a month')
            self.assertEqual(call_args_list_1['email_type'], 'project_still_in_draft')
            self.assertEqual(call_args_list_1['to'], [self.user_1.email])
            self.assertEqual(call_args_list_1['context'], {'project_name': 'Draft project 1'})

            call_args_list_2 = send_mail_wrapper.call_args_list[1][1]
            self.assertEqual(call_args_list_2['subject'], 'Project has been in draft state for over a month')
            self.assertEqual(call_args_list_2['email_type'], 'project_still_in_draft')
            self.assertEqual(call_args_list_2['to'], [self.user_2.email])
            self.assertEqual(call_args_list_2['context'], {'project_name': 'Draft project 2'})

        # init
        send_mail_wrapper.call_args_list = _CallList()

        with override_settings(EMAIL_SENDING_PRODUCTION=False):
            project_still_in_draft_notification.apply()

            # task should send email about Draft project 1
            self.assertEqual(len(send_mail_wrapper.call_args_list), 1)

            call_args_list = send_mail_wrapper.call_args_list[0][1]
            self.assertEqual(call_args_list['subject'], 'Project has been in draft state for over a month')
            self.assertEqual(call_args_list['email_type'], 'project_still_in_draft')
            self.assertEqual(call_args_list['to'], [self.user_1.email])
            self.assertEqual(call_args_list['context'], {'project_name': 'Draft project 1'})

    @mock.patch('project.tasks.send_mail_wrapper', return_value=None)
    def test_published_projects_updated_long_ago(self, send_mail_wrapper):
        now = timezone.now()

        with freeze_time(now - timezone.timedelta(days=200)):
            draft_project_1 = Project.objects.create(name='Draft project 1', public_id='')
            draft_project_1.team.add(self.profile_1)

            # make a published project without API calls
            published_project_1 = Project.objects.create(
                name='Published project 1', data=self.published_project_data, public_id='1234')
            published_project_1.team.add(self.profile_1)

        with freeze_time(now - timezone.timedelta(days=190)):
            draft_project_2 = Project.objects.create(name='Draft project 2', public_id='')
            draft_project_2.team.add(self.profile_2)

            # make a published project without API calls
            published_project_2 = Project.objects.create(
                name='Published project 2', data=self.published_project_data, public_id='2345')
            published_project_2.team.add(self.profile_2)

        with freeze_time(now - timezone.timedelta(days=100)):
            # make a published project without API calls
            published_project_3 = Project.objects.create(
                name='Published project 3', data=self.published_project_data, public_id='3456')
            published_project_3.team.add(self.profile_3)

        with override_settings(EMAIL_SENDING_PRODUCTION=True):
            published_projects_updated_long_ago.apply()

            # task should send emails about Published project 1 and Published project 2
            self.assertEqual(len(send_mail_wrapper.call_args_list), 2)

            call_args_list_1 = send_mail_wrapper.call_args_list[0][1]
            self.assertEqual(call_args_list_1['subject'], 'Published project last updated over 6 months')
            self.assertEqual(call_args_list_1['email_type'], 'published_project_updated_long_ago')
            self.assertEqual(call_args_list_1['to'], [self.user_1.email])
            self.assertEqual(call_args_list_1['context'], {'project_name': 'Published project 1'})

            call_args_list_2 = send_mail_wrapper.call_args_list[1][1]
            self.assertEqual(call_args_list_2['subject'], 'Published project last updated over 6 months')
            self.assertEqual(call_args_list_2['email_type'], 'published_project_updated_long_ago')
            self.assertEqual(call_args_list_2['to'], [self.user_2.email])
            self.assertEqual(call_args_list_2['context'], {'project_name': 'Published project 2'})

        # init
        send_mail_wrapper.call_args_list = _CallList()

        with override_settings(EMAIL_SENDING_PRODUCTION=False):
            published_projects_updated_long_ago.apply()

            # task should send email about Published project 1
            self.assertEqual(len(send_mail_wrapper.call_args_list), 1)

            call_args_list = send_mail_wrapper.call_args_list[0][1]
            self.assertEqual(call_args_list['subject'], 'Published project last updated over 6 months')
            self.assertEqual(call_args_list['email_type'], 'published_project_updated_long_ago')
            self.assertEqual(call_args_list['to'], [self.user_1.email])
            self.assertEqual(call_args_list['context'], {'project_name': 'Published project 1'})
