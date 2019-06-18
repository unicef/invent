from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User

from country.models import Country
from user.models import Organisation, UserProfile
from project.models import Project, ProjectImport

from project.tests.setup import MockRequest


class TestProjectImportAdmin(TestCase):

    def setUp(self):
        settings.MEDIA_ROOT = '/tmp/'  # so tests won't litter filesystem
        settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
        with self.settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage'):
            # Admin for testing
            self.request = MockRequest()
            self.site = AdminSite()

            # Create admin user
            self.test_admin = User.objects.create_superuser(
                username='test_admin',
                password='test',
                email='test_admin@test.com',
            )
            self.client.force_login(self.test_admin)

            # Create test user
            self.test_user = User.objects.create_user(
                username='test_user',
                password='test',
                email='test_user@test.com',
            )
            UserProfile.objects.create(user=self.test_user, account_type=UserProfile.IMPLEMENTER)

            # CSV data
            self.csv_content = ('Project,Owner,Owner email,Country,Organisation\n'
                                'Proj1,Owner Owen,owen@owner.com,Kenya,Org1\n'
                                'Proj2,Test Owner,test_user@test.com,Kenya,Org2\n'
                                'Proj3,Test Owner,test_user@test.com,Invalidcountry,Org2\n'
                                'Proj4,Test Owner,invalidemail,Invalidcountry,Org2\n'
                                'Proj11,Owner Owen,owen@owner.com,Kenya,Org11\n')

    def test_project_import_wrong_ext(self):
        # Upload csv
        csv_file = SimpleUploadedFile('a.asdf', self.csv_content.encode())
        url = reverse('admin:project_projectimport_add')
        data = {
            'csv': csv_file
        }
        response = self.client.post(url, data, format='multipart', follow=True)
        self.assertTrue('Only CSV format is accepted.' in response.content.decode('utf-8'))

    def test_project_import_success(self):
        csv_content = ('Project,Owner,Owner email,Country,Organisation,Description\n'
                       'Proj1,Owner Owen,owen@owner.com,Kenya,Org1,Some desc\n')
        # Upload csv
        csv_file = SimpleUploadedFile('a.csv', csv_content.encode())
        url = reverse('admin:project_projectimport_add')
        data = {
            'csv': csv_file
        }
        response = self.client.post(url, data, format='multipart', follow=True)
        self.assertEqual(response.status_code, 200)

        # Map fields
        project_import = ProjectImport.objects.all().first()
        url = reverse('admin:project_projectimport_change', args=[project_import.id])
        data = {
            'project_name': '0',
            'owner_name': '1',
            'owner_email': '2',
            'country': '3',
            'description': '5',
            'organisation': '4',
        }
        response = self.client.post(url, data, follow=True)
        project_import.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project_import.mapping, data)
        self.assertEqual(project_import.status, True)

        # Check results page
        url = reverse('admin:project_projectimport_change', args=[project_import.id])
        response = self.client.get(url)
        self.assertTrue('Proj1' in response.content.decode('utf-8'))

    def test_project_import_success_no_country_no_org(self):
        csv_content = ('Project,Owner,Owner email,Organisation\n'
                       'Proj1,Owner Owen,owen@owner.com,Org1\n')
        # Upload csv
        csv_file = SimpleUploadedFile('a.csv', csv_content.encode())
        url = reverse('admin:project_projectimport_add')
        data = {
            'csv': csv_file
        }
        response = self.client.post(url, data, format='multipart', follow=True)
        self.assertEqual(response.status_code, 200)

        # Map fields
        project_import = ProjectImport.objects.all().first()
        url = reverse('admin:project_projectimport_change', args=[project_import.id])
        data = {
            'project_name': '0',
            'owner_name': '1',
            'owner_email': '2',
            'country': '',
            'description': '',
            'organisation': '',
        }
        response = self.client.post(url, data, follow=True)
        project_import.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project_import.mapping, data)
        self.assertEqual(project_import.status, True)

        # Check results page
        url = reverse('admin:project_projectimport_change', args=[project_import.id])
        response = self.client.get(url)
        self.assertTrue('Proj1' in response.content.decode('utf-8'))

    def test_project_import_some_fails(self):
        # Upload csv
        csv_file = SimpleUploadedFile('a.csv', self.csv_content.encode())
        url = reverse('admin:project_projectimport_add')
        data = {
            'csv': csv_file
        }
        response = self.client.post(url, data, format='multipart', follow=True)
        self.assertEqual(response.status_code, 200)

        # Map fields
        project_import = ProjectImport.objects.all().first()
        url = reverse('admin:project_projectimport_change', args=[project_import.id])
        data = {
            'project_name': '0',
            'owner_name': '1',
            'owner_email': '2',
            'country': '3',
            'description': '',
            'organisation': '4',
        }
        response = self.client.post(url, data, follow=True)
        project_import.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project_import.mapping, data)

        # Check results page
        url = reverse('admin:project_projectimport_change', args=[project_import.id])
        response = self.client.get(url)
        self.assertTrue('Line 3, Invalidcountry: No such country.' in response.content.decode('utf-8'))
        self.assertTrue('Line 4, Invalidcountry: No such country.' in response.content.decode('utf-8'))
        self.assertTrue('Line 4, invalidemail: Enter a valid email address.' in response.content.decode('utf-8'))

        self.assertTrue(Project.objects.filter(name='Proj1').exists())
        self.assertTrue(Project.objects.filter(name='Proj2').exists())
        self.assertFalse(Project.objects.filter(name='Proj3').exists())
        self.assertFalse(Project.objects.filter(name='Proj4').exists())
        self.assertTrue(Organisation.objects.filter(name='Org1').exists())
        self.assertTrue(Organisation.objects.filter(name='Org2').exists())
        self.assertEquals(Organisation.objects.get(name='Org1').id,
                          Project.objects.get(name='Proj1').draft['organisation'])
        self.assertEquals(Organisation.objects.get(name='Org2').id,
                          Project.objects.get(name='Proj2').draft['organisation'])
        self.assertEquals(Project.objects.get(name='Proj1').draft['country_name'], 'Kenya')
        self.assertEquals(Project.objects.get(name='Proj1').draft['country'], Country.objects.get(name='Kenya').id)
        self.assertEquals(Project.objects.get(name='Proj2').draft['country_name'], 'Kenya')
        self.assertEquals(Project.objects.get(name='Proj2').draft['country'], Country.objects.get(name='Kenya').id)
        self.assertTrue(UserProfile.objects.filter(user__email='owen@owner.com').exists())
        self.assertEquals(UserProfile.objects.filter(user__email='owen@owner.com').first(),
                          Project.objects.get(name='Proj1').team.first())
        self.assertEquals(UserProfile.objects.filter(user__email='test_user@test.com').first(),
                          Project.objects.get(name='Proj2').team.first())
        self.assertIn('Your login credentials are', mail.outbox[0].alternatives[0][0]),
        self.assertIn('owen@owner.com', mail.outbox[0].alternatives[0][0]),
        self.assertIn('/en/-/projects/{}/edit'.format(Project.objects.get(name='Proj1').id),
                      mail.outbox[0].alternatives[0][0])
        self.assertIn('/en/-/projects/{}/edit'.format(Project.objects.get(name='Proj11').id),
                      mail.outbox[0].alternatives[0][0])
        self.assertIn('/en/-/projects/{}/edit'.format(Project.objects.get(name='Proj2').id),
                      mail.outbox[1].alternatives[0][0])
        # notifying the superusers about every successful project import
        # should be 3, Proj1, Proj2 and Proj11
        self.assertIn('The projects listed below have been imported.', mail.outbox[-1].alternatives[0][0]),
        self.assertIn('/en/-/projects/{}/edit'.format(Project.objects.get(name='Proj1').id),
                      mail.outbox[-1].alternatives[0][0])
        self.assertIn('/en/-/projects/{}/edit'.format(Project.objects.get(name='Proj2').id),
                      mail.outbox[-1].alternatives[0][0])
        self.assertIn('/en/-/projects/{}/edit'.format(Project.objects.get(name='Proj11').id),
                      mail.outbox[-1].alternatives[0][0])
        self.assertIn('Proj1', project_import.imported)
        self.assertIn('Proj2', project_import.imported)
        self.assertIn('Line 3, Invalidcountry: No such country.', project_import.failed)
        self.assertIn('Line 4, Invalidcountry: No such country.', project_import.failed)
        self.assertIn('Line 4, invalidemail: Enter a valid email address.', project_import.failed)
