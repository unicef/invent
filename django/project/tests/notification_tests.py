from unittest import mock

from django.contrib.auth.models import User
from django.utils import timezone
from freezegun import freeze_time

from project.models import Project
from project.tasks import project_still_in_draft_notification
from project.tests.setup import SetupTests
from user.models import UserProfile


class ProjectNotificationTests(SetupTests):

    @mock.patch('project.tasks.send_mail_wrapper', return_value=None)
    def test_project_still_in_draft_notification(self, send_mail_wrapper):
        now = timezone.now()

        user_1 = User.objects.create(username='bh_1', email='bh+1@pulilab.com')
        profile_1 = UserProfile.objects.create(user=user_1)
        user_2 = User.objects.create(username='bh_2', email='bh+2@pulilab.com')
        profile_2 = UserProfile.objects.create(user=user_2)
        user_3 = User.objects.create(username='bh_3', email='bh+3@pulilab.com')
        profile_3 = UserProfile.objects.create(user=user_3)

        with freeze_time(now - timezone.timedelta(days=40)):
            draft_project_1 = Project.objects.create(name='Draft project 1', public_id='')
            draft_project_1.team.add(profile_1)

            # make a published project without API calls
            data = dict(country=self.country.id, country_office=self.country_office.id, organisation=self.org.id,
                        hsc_challenges=[1, 2], platforms=[1, 2], capability_categories=[], capability_levels=[],
                        capability_subcategories=[])
            published_project = Project.objects.create(name='Published project 1', data=data, public_id='1234')
            published_project.team.add(profile_1)

        with freeze_time(now - timezone.timedelta(days=32)):
            draft_project_2 = Project.objects.create(name='Draft project 2', public_id='')
            draft_project_2.team.add(profile_2)

        with freeze_time(now - timezone.timedelta(days=20)):
            draft_project_3 = Project.objects.create(name='Draft project 3', public_id='')
            draft_project_3.team.add(profile_3)

        project_still_in_draft_notification.apply()

        # task should send emails about Draft project 1 and Draft project 2
        self.assertEqual(len(send_mail_wrapper.call_args_list), 2)

        call_args_list_1 = send_mail_wrapper.call_args_list[0][1]
        self.assertEqual(call_args_list_1['subject'], 'Project has been in draft state for over a month')
        self.assertEqual(call_args_list_1['email_type'], 'project_still_in_draft')
        self.assertEqual(call_args_list_1['to'], [user_1.email])
        self.assertEqual(call_args_list_1['context'], {'project_name': 'Draft project 1'})

        call_args_list_2 = send_mail_wrapper.call_args_list[1][1]
        self.assertEqual(call_args_list_2['subject'], 'Project has been in draft state for over a month')
        self.assertEqual(call_args_list_2['email_type'], 'project_still_in_draft')
        self.assertEqual(call_args_list_2['to'], [user_2.email])
        self.assertEqual(call_args_list_2['context'], {'project_name': 'Draft project 2'})
