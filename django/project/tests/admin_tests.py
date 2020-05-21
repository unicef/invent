from allauth.account.models import EmailConfirmation
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Permission

from country.models import Country
from project.admin import ProjectAdmin, DigitalStrategyAdmin, TechnologyPlatformAdmin
from user.models import UserProfile
from project.models import Project, DigitalStrategy, TechnologyPlatform

from project.tests.setup import MockRequest


class TestAdmin(TestCase):
    def setUp(self):
        self.request = MockRequest()
        self.site = AdminSite()
        self.user = User.objects.create_user(username="alma", password="korte")
        self.userprofile = UserProfile.objects.create(user=self.user, name="almakorte")

        url = reverse('rest_register')
        data = {'email': 'test_user@gmail.com',
                'password1': '123456hetNYOLC',
                'password2': '123456hetNYOLC'}
        self.client.post(url, data)

    def test_admin(self):
        admin = DigitalStrategyAdmin(DigitalStrategy, self.site)
        self.assertEqual(admin.get_queryset(self.request).count(), DigitalStrategy.all_objects.all().count())
        translate_bools = ['is_translated_{}'.format(language_code) for language_code, _ in settings.LANGUAGES]
        self.assertEqual(admin.get_list_display(self.request), ['__str__', 'is_active'] + translate_bools)
        admin.list_display = ['__str__', 'is_active']
        self.assertEqual(admin.get_list_display(self.request), ['__str__', 'is_active'])

    def xtest_created_notification(self):  # pragma: no cover
        initial_email_count = len(mail.outbox)
        user_2 = User.objects.create_superuser(username='test_2', email='test2@test.test', password='a')
        UserProfile.objects.create(user=user_2, language='fr')

        tpa = TechnologyPlatformAdmin(TechnologyPlatform, self.site)

        ModelForm = tpa.get_form(self.request)
        data = {'name': 'New technology platform',
                'is_active': True}
        form = ModelForm(data)

        self.assertTrue(form.is_valid(), form.errors)
        tpa.save_form(self.request, form, False)

        self.assertEqual(len(mail.outbox),
                         initial_email_count + UserProfile.objects.all().count())

        first_en = '<meta http-equiv="content-language" content="en">' in mail.outbox[-2].message().as_string()
        en_index = -2 if first_en else -1
        fr_index = -1 if first_en else -2

        outgoing_en_email_text = mail.outbox[en_index].message().as_string()

        self.assertIn('New technology platform was created: {}'.format(str(form.instance)), outgoing_en_email_text)
        self.assertIn('<meta http-equiv="content-language" content="en">', outgoing_en_email_text)

        outgoing_fr_email_text = mail.outbox[fr_index].message().as_string()
        self.assertIn('<meta http-equiv="content-language" content="fr">', outgoing_fr_email_text)

    def xtest_modified_notification(self):  # pragma: no cover
        initial_email_count = len(mail.outbox)
        user_2 = User.objects.create_superuser(username='test_2', email='test2@test.test', password='a')
        UserProfile.objects.create(user=user_2, language='fr')

        tpa = TechnologyPlatformAdmin(TechnologyPlatform, self.site)
        technology_platform = TechnologyPlatform(name='Test platform')

        ModelForm = tpa.get_form(self.request, technology_platform)
        data = {'name': 'something different',
                'is_active': technology_platform.is_active}
        form = ModelForm(data, instance=technology_platform)

        self.assertTrue(form.is_valid(), form.errors)
        tpa.save_form(self.request, form, True)

        self.assertEqual(len(mail.outbox),
                         initial_email_count + UserProfile.objects.all().count())

        first_en = '<meta http-equiv="content-language" content="en">' in mail.outbox[-2].message().as_string()
        en_index = -2 if first_en else -1
        fr_index = -1 if first_en else -2

        outgoing_en_email_text = mail.outbox[en_index].message().as_string()

        self.assertIn('Technology Platform - {} was changed'.format(str(form.instance)), outgoing_en_email_text)
        self.assertIn('<meta http-equiv="content-language" content="en">', outgoing_en_email_text)

        outgoing_fr_email_text = mail.outbox[fr_index].message().as_string()
        self.assertIn('<meta http-equiv="content-language" content="fr">', outgoing_fr_email_text)

    def test_modified_but_not_changed(self):
        initial_email_count = len(mail.outbox)

        tpa = TechnologyPlatformAdmin(TechnologyPlatform, self.site)
        technology_platform = TechnologyPlatform(name='Test platform')

        ModelForm = tpa.get_form(self.request, technology_platform)
        data = {'name': technology_platform.name,
                'name_en': technology_platform.name,
                'is_active': technology_platform.is_active}
        form = ModelForm(data, instance=technology_platform)

        self.assertTrue(form.is_valid(), form.errors)
        self.assertFalse(form.has_changed(), form.changed_data)
        tpa.save_form(self.request, form, True)

        self.assertEqual(len(mail.outbox), initial_email_count)

    def test_project_admin_custom_fields(self):
        pa = ProjectAdmin(Project, self.site)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.request.user = self.user

        p = Project.objects.create(name="test change view", draft=dict(country=Country.objects.get(id=1).id))
        p.team.add(self.userprofile.id)

        self.assertEqual(pa.get_country(p), Country.objects.get(id=1))
        self.assertEqual(pa.get_team(p), str(self.userprofile))
        self.assertFalse(pa.get_published(p))
        self.assertFalse(pa.has_add_permission(self.request))

    def test_project_admin_queryset(self):
        pa = ProjectAdmin(Project, self.site)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.request.user = self.user

        country = Country.objects.get(id=1)
        country_id = country.id
        p_not_in_country = Project.objects.create(name="not in country")
        p1_draft = Project.objects.create(name="draft in country")
        p1_draft.draft['country'] = country_id
        p1_draft.save()
        p2_published = Project.objects.create(name="published in country")
        p2_published.draft['country'] = country_id
        p2_published.data['country'] = country_id
        p2_published.save()

        # superuser sees it all
        self.assertEqual(pa.get_queryset(self.request).count(), 3)

        # let's degrade him to a country admin
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        country.users.add(self.user.userprofile)

        self.assertEqual(pa.get_queryset(self.request).count(), 2)
        self.assertTrue(pa.get_queryset(self.request).filter(name=p1_draft.name).exists())
        self.assertTrue(pa.get_queryset(self.request).filter(name=p2_published.name).exists())
        self.assertFalse(pa.get_queryset(self.request).filter(name=p_not_in_country.name).exists())

    def test_project_admin_changeform_view(self):
        request = MockRequest()
        request.method = 'GET'
        request.POST = {}
        request.META = {'SCRIPT_NAME': 'from_test'}
        request.resolver_match = False

        content_type = ContentType.objects.get(app_label=Project._meta.app_label,
                                               model=Project._meta.model_name)
        change_permission = Permission.objects.get(content_type=content_type,
                                                   codename='change_{}'.format(Project._meta.model_name))

        p = Project.objects.create(name="test change view")
        self.user.user_permissions.add(change_permission)
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        request.user = self.user
        pa = ProjectAdmin(Project, self.site)
        response = pa.changeform_view(request, object_id=str(p.id))
        self.assertTrue(isinstance(response, TemplateResponse))
