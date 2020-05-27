from django.test import TestCase
from django.utils.translation import override
from django.core.cache import cache
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from project.models import TechnologyPlatform, DigitalStrategy, HealthFocusArea, HealthCategory, HSCChallenge, HSCGroup
from user.models import UserProfile
from user.tests import create_profile_for_user


class TestModelTranslations(TestCase):
    def setUp(self):
        # Create a test user with profile.
        url = reverse('rest_register')
        data = {
            'email': 'test_user@gmail.com',
            'password1': '123456hetNYOLC',
            'password2': '123456hetNYOLC'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

        create_profile_for_user(response)

        # Log in the user.
        data = {
            'username': 'test_user@gmail.com',
            'password': '123456hetNYOLC'}
        response = self.client.post(reverse('api_token_auth'), data)
        self.assertEqual(response.status_code, 200)
        self.test_user_key = response.json().get('token')
        self.test_user_client = APIClient(HTTP_AUTHORIZATION='Token {}'.format(self.test_user_key), format='json')
        user_profile = UserProfile.objects.get(id=response.json().get('user_profile_id'))
        self.user = user_profile.user

        self.platform = TechnologyPlatform.objects.create(name='Test platform')
        self.platform.name_en = 'English name'
        self.platform.name_fr = 'French name'
        self.platform.save()

    def test_model_translations(self):
        self.assertEqual(self.platform.name, 'English name')

        with override('en'):
            self.assertEqual(self.platform.name, 'English name')

        with override('fr'):
            self.assertEqual(self.platform.name, 'French name')

    def test_translation_through_api(self):
        TechnologyPlatform.objects.exclude(id=self.platform.id).delete()
        cache.clear()

        url = reverse('get-project-structure')

        # Getting the english version
        response = self.test_user_client.get(url, HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['technology_platforms'][0]['name'], 'English name')

        # Getting the french version
        response = self.test_user_client.get(url, HTTP_ACCEPT_LANGUAGE='fr')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['technology_platforms'][0]['name'], 'French name')

    def test_innermost_translation(self):
        DigitalStrategy.objects.all().delete()
        HealthFocusArea.objects.all().delete()
        HealthCategory.objects.all().delete()
        cache.clear()

        strategy = DigitalStrategy.objects.create(name='Test strategy', group=DigitalStrategy.GROUP_CHOICES[0][0])
        strategy.name_en = 'English name'
        strategy.name_fr = 'French name'
        strategy.save()

        child_strategy = DigitalStrategy.objects.create(name='Child strategy', parent=strategy,
                                                        group=DigitalStrategy.GROUP_CHOICES[0][0])
        child_strategy.name_en = 'Child name'
        child_strategy.name_fr = 'Omlette du fromage'
        child_strategy.save()

        health_category = HealthCategory.objects.create(name='Parent category')
        health_category.name_en = 'English name'
        health_category.name_fr = 'French name'
        health_category.save()

        health_focus_area = HealthFocusArea.objects.create(name='Health focus area', health_category=health_category)
        health_focus_area.name_en = 'English area'
        health_focus_area.name_fr = 'French area'
        health_focus_area.save()

        url = reverse('get-project-structure')
        # Getting the english version
        response = self.test_user_client.get(url, HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['strategies'][0],
                         {'name': 'Client',
                          'subGroups': [{'id': strategy.id,
                                         'name': 'English name',
                                         'strategies': [{'id': child_strategy.id,
                                                         'name': 'Child name'}]}]})
        self.assertEqual(response.json()['health_focus_areas'][0],
                         {'id': health_category.id,
                          'name': 'English name',
                          'health_focus_areas': [{'id': health_focus_area.id,
                                                  'name': 'English area'}]})

        # Getting the french version
        response = self.test_user_client.get(url, HTTP_ACCEPT_LANGUAGE='fr')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['strategies'][0],
                         {'name': 'Client',
                          'subGroups': [{'id': strategy.id,
                                         'name': 'French name',
                                         'strategies': [{'id': child_strategy.id,
                                                         'name': 'Omlette du fromage'}]}]})
        self.assertEqual(response.json()['health_focus_areas'][0],
                         {'id': health_category.id,
                          'name': 'French name',
                          'health_focus_areas': [{'id': health_focus_area.id,
                                                  'name': 'French area'}]})

    def test_health_system_challenges(self):
        self.maxDiff = None
        HSCChallenge.objects.all().delete()
        HSCGroup.objects.all().delete()
        cache.clear()

        hsc_group = HSCGroup.objects.create(name='First group')
        hsc_group.name_en = 'First group'
        hsc_group.name_fr = 'Omlette du fromage'
        hsc_group.save()

        hsc = HSCChallenge.objects.create(name='Solve an issue', group=hsc_group)
        hsc_2 = HSCChallenge.objects.create(name='Other problem appeared', group=hsc_group)
        hsc_3 = HSCChallenge.objects.create(name='Third failure here', group=hsc_group)

        hsc.name_en = 'Solve an issue'
        hsc.name_fr = "l'Solve an issue"
        hsc.save()

        url = reverse('get-project-structure')
        response = self.test_user_client.get(url, HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['hsc_challenges'][0],
                         {'name': 'First group',
                          'challenges': [
                              {'id': hsc_2.id,
                               'challenge': 'Other problem appeared'},
                              {'id': hsc.id,
                               'challenge': 'Solve an issue'},
                              {'id': hsc_3.id,
                               'challenge': 'Third failure here'}
                          ]})

        response = self.test_user_client.get(url, HTTP_ACCEPT_LANGUAGE='fr')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['hsc_challenges'][0],
                         {'name': 'Omlette du fromage',
                          'challenges': [
                              {'id': hsc.id,
                               'challenge': "l'Solve an issue"},
                              {'id': hsc_2.id,
                               'challenge': 'Other problem appeared'},
                              {'id': hsc_3.id,
                               'challenge': 'Third failure here'}
                          ]})
