import copy
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

    @mock.patch('project.tasks.send_mail_wrapper', return_value=None)
    def test_project_still_in_draft_notification(self, send_mail_wrapper):
        now = timezone.now()

        with freeze_time(now - timezone.timedelta(days=40)):
            # task should pick this up
            draft_project_1 = Project.objects.create(name='Draft project 1', public_id='')
            draft_project_1.team.add(self.profile_1)

            # make a published project without API calls, task shouldn't pick this up
            published_project = Project.objects.create(
                name='Published project 1', data=self.published_project_data, public_id='1234')
            published_project.team.add(self.profile_1)

        with freeze_time(now - timezone.timedelta(days=32)):
            # task should pick this up
            draft_project_2 = Project.objects.create(name='Draft project 2', public_id='')
            draft_project_2.team.add(self.profile_2)

        with freeze_time(now - timezone.timedelta(days=20)):
            # task shouldn't pick this up, it is not over 30 days
            draft_project_3 = Project.objects.create(name='Draft project 3', public_id='')
            draft_project_3.team.add(self.profile_3)

        with freeze_time(now - timezone.timedelta(days=45)):
            draft_project_4 = Project.objects.create(name='Draft project 4', public_id='')
            draft_project_4.team.add(self.profile_4)

            # draft_project_4 should be excluded because it is in "Scale and Handover" state
            draft_project_4.draft['donor_custom_answers'] = {
                self.unicef.id: {self.custom_question.id: ['Scale and Handover']}
            }
            draft_project_4.save()

            draft_project_5 = Project.objects.create(name='Draft project 5', public_id='')
            draft_project_5.team.add(self.profile_5)

            # draft_project_5 should be excluded because it is in "Discontinued" state
            draft_project_5.draft['donor_custom_answers'] = {
                self.unicef.id: {self.custom_question.id: ['Discontinued']}
            }
            draft_project_5.save()

            # task should pick this up
            draft_project_6 = Project.objects.create(name='Draft project 6', public_id='')
            draft_project_6.team.add(self.profile_2)

        with override_settings(EMAIL_SENDING_PRODUCTION=True):
            project_still_in_draft_notification.apply()

            # task should send emails about Draft project 1 and Draft project 2
            self.assertEqual(len(send_mail_wrapper.call_args_list), 2)

            for call in send_mail_wrapper.call_args_list:
                call_args = call[1]
                self.assertEqual(call_args['email_type'], 'reminder_common_template')
                self.assertEqual(call_args['language'], 'en')
                if call_args['to'] == self.user_1.email:
                    # user_1 should receive notifications about draft project 1
                    self.assertEqual(call_args['context']['name'], self.profile_1.name)
                    self.assertEqual(len(call_args['context']['projects']), 1)
                    self.assertIn(draft_project_1, call_args['context']['projects'])
                else:
                    # user_2 should receive notifications about draft project 2 and draft project 6
                    self.assertEqual(call_args['context']['name'], self.profile_2.name)
                    self.assertEqual(len(call_args['context']['projects']), 2)
                    self.assertIn(draft_project_2, call_args['context']['projects'])
                    self.assertIn(draft_project_6, call_args['context']['projects'])

        # init
        send_mail_wrapper.call_args_list = _CallList()

        with override_settings(EMAIL_SENDING_PRODUCTION=False):
            project_still_in_draft_notification.apply()

            # task should send email about Draft project 1
            self.assertEqual(len(send_mail_wrapper.call_args_list), 1)

            call_args_list = send_mail_wrapper.call_args_list[0][1]
            self.assertEqual(call_args_list['email_type'], 'reminder_common_template')
            self.assertEqual(call_args_list['language'], 'en')
            self.assertEqual(call_args_list['to'], self.user_1.email)
            self.assertEqual(len(call_args_list['context']['projects']), 1)
            self.assertIn(draft_project_1, call_args_list['context']['projects'])

    @mock.patch('project.tasks.send_mail_wrapper', return_value=None)
    def test_published_projects_updated_long_ago(self, send_mail_wrapper):
        now = timezone.now()

        with freeze_time(now - timezone.timedelta(days=200)):
            draft_project_1 = Project.objects.create(name='Draft project 1', public_id='')
            draft_project_1.team.add(self.profile_1)

            # make a published project without API calls, task should pick this up
            published_project_1 = Project.objects.create(
                name='Published project 1', data=self.published_project_data, public_id='1111')
            published_project_1.team.add(self.profile_1)

        with freeze_time(now - timezone.timedelta(days=190)):
            draft_project_2 = Project.objects.create(name='Draft project 2', public_id='')
            draft_project_2.team.add(self.profile_2)

            # task should pick this up
            published_project_2 = Project.objects.create(
                name='Published project 2', data=self.published_project_data, public_id='2222')
            published_project_2.team.add(self.profile_2)

        with freeze_time(now - timezone.timedelta(days=100)):
            # task shouldn't pick this up
            published_project_3 = Project.objects.create(
                name='Published project 3', data=self.published_project_data, public_id='3333')
            published_project_3.team.add(self.profile_3)

        with freeze_time(now - timezone.timedelta(days=210)):
            # published_project_4 should be excluded because it is in "Discontinued" state
            data = copy.deepcopy(self.published_project_data)
            data['donor_custom_answers'] = {
                self.unicef.id: {self.custom_question.id: ['Discontinued']}
            }

            published_project_4 = Project.objects.create(name='Published project 4', data=data, public_id='4444')
            published_project_4.team.add(self.profile_4)

            # task should pick this up
            published_project_5 = Project.objects.create(
                name='Published project 5', data=self.published_project_data, public_id='5555')
            published_project_5.team.add(self.profile_2)

        with override_settings(EMAIL_SENDING_PRODUCTION=True):
            published_projects_updated_long_ago.apply()

            # task should send emails about Published project 1 and Published project 2
            self.assertEqual(len(send_mail_wrapper.call_args_list), 2)

            for call in send_mail_wrapper.call_args_list:
                call_args = call[1]
                self.assertEqual(call_args['email_type'], 'reminder_common_template')
                self.assertEqual(call_args['language'], 'en')
                if call_args['to'] == self.user_1.email:
                    # user_1 should receive notifications about published project 1
                    self.assertEqual(call_args['context']['name'], self.profile_1.name)
                    self.assertEqual(len(call_args['context']['projects']), 1)
                    self.assertIn(published_project_1, call_args['context']['projects'])
                else:
                    # user_2 should receive notifications about published project 2
                    self.assertEqual(call_args['context']['name'], self.profile_2.name)
                    self.assertEqual(len(call_args['context']['projects']), 2)
                    self.assertIn(published_project_2, call_args['context']['projects'])
                    self.assertIn(published_project_5, call_args['context']['projects'])

        # init
        send_mail_wrapper.call_args_list = _CallList()

        with override_settings(EMAIL_SENDING_PRODUCTION=False):
            published_projects_updated_long_ago.apply()

            # task should send email about Published project 1
            self.assertEqual(len(send_mail_wrapper.call_args_list), 1)

            call_args_list = send_mail_wrapper.call_args_list[0][1]
            self.assertEqual(call_args_list['email_type'], 'reminder_common_template')
            self.assertEqual(call_args_list['to'], self.user_1.email)
            self.assertIn(published_project_1, call_args_list['context']['projects'])
