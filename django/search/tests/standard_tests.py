import copy

from django.urls import reverse
from rest_framework import status

from country.models import Donor, DonorCustomQuestion, CountryCustomQuestion
from project.models import Project, DigitalStrategy, HealthFocusArea, HSCChallenge
from project.tests.setup import SetupTests


class SearchTests(SetupTests):
    def setUp(self):
        super(SearchTests, self).setUp()
        # create draft
        url = reverse("project-create", kwargs=dict(country_office_id=self.country_office.id))
        project_data2 = copy.deepcopy(self.project_data)
        project_data2['project'].update(name="phrase3 phrase5 overview")
        project_data2['project'].update(country=self.country_id, government_investor=2)
        project_data2['project'].update(platforms=[1, 2])
        project_data2['project'].update(dhis=[118, 171])
        self.d1cq = DonorCustomQuestion.objects.create(question="test 1", private=True, donor_id=self.d1.id)
        self.d2cq = DonorCustomQuestion.objects.create(question="test 2", private=True, donor_id=self.d2.id)
        project_data2['donor_custom_answers'] = {self.d1.id: [{"question_id": self.d1cq.id, "answer": ["answer1"]}],
                                                 self.d2.id: [{"question_id": self.d2cq.id, "answer": ["answer2"]}]}
        self.ccq1 = CountryCustomQuestion.objects.create(question="ctest q 1", private=True, country_id=self.country_id)
        self.ccq2 = CountryCustomQuestion.objects.create(question="ctest q 2", private=True, country_id=self.country_id)
        project_data2['country_custom_answers'] = [{"question_id": self.ccq1.id, "answer": ["answer country 1"]},
                                                   {"question_id": self.ccq2.id, "answer": ["answer country 2"]}]
        response = self.test_user_client.post(url, project_data2, format="json")
        self.assertEqual(response.status_code, 201)
        project_id = response.json()['id']

        # publish it
        url = reverse("project-publish", kwargs=dict(project_id=project_id,
                                                     country_office_id=self.country_office.id))
        response = self.test_user_client.put(url, project_data2, format="json")
        self.assertEqual(response.status_code, 200)

        self.project2 = Project.objects.get(id=project_id)
        self.project2.approve()
        self.project2_id = project_id

    def test_search_no_results(self):
        url = reverse("search-project-list")
        data = {"q": "phrase2"}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']['projects']), 0)
        self.assertEqual(response.json()['count'], 0)
        self.assertEqual(response.json()['results'],
                         {'projects': [], 'search_term': 'phrase2', 'search_in': [], 'type': 'map'})

    def test_no_query_params_returns_all_published_projects(self):
        url = reverse("search-project-list")
        response = self.test_user_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], Project.objects.published_only().count())

    def test_only_search_term_without_search_in(self):
        url = reverse("search-project-list")
        data = {"q": "phrase3"}  # PROJECT NAME
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['count'] >= 1)

        data = {"q": "org1"}  # ORGANISATION
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['count'] >= 1)

        data = {"q": "Hungary"}  # COUNTRY
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['count'] >= 1)

        data = {"q": "overview"}  # OVERVIEW
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['count'] >= 1)

    def test_only_search_term_with_search_in(self):
        url = reverse("search-project-list")
        data = {"q": "phrase3", "in": "name"}  # PROJECT NAME
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['count'] >= 1)

        data = {"q": "org1", "in": "name"}  # ORGANISATION
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

        data = {"q": "Hungary", "in": "name"}  # COUNTRY
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

        data = {"q": "dist1", "in": "name"}  # LOCATION
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

        data = {"q": "partner1", "in": "name"}  # PARTNER
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

        data = {"q": "donor1", "in": "name"}  # DONOR
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_found_in(self):
        url = reverse("search-project-list")
        data = {"q": "overview", "found": ""}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['count'] >= 1)
        self.assertTrue('found_in' in response.json()['results'])
        self.assertTrue(self.project2_id in response.json()['results']['found_in']['name'])
        self.assertTrue(self.project2_id in response.json()['results']['found_in']['overview'])
        self.assertTrue(self.project_id in response.json()['results']['found_in']['overview'])

    def test_query_length(self):
        url = reverse("search-project-list")
        data = {"q": "o"}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ["Search term must be at least two characters long."])

    def test_filter_country(self):
        url = reverse("search-project-list")
        data = {"country": self.country_id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

        data = {"country": self.country_id + 999}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_filter_country_office(self):
        url = reverse("search-project-list")
        data = {"co": self.country_office.id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.json()['count'], 2)

        data = {"co": self.country_office.id + 999}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.json()['count'], 0)

    def test_filter_and_search(self):
        url = reverse("search-project-list")
        data = {"q": "overview", "in": "name", "country": self.country_id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_filter_list_results(self):
        url = reverse("search-project-list")
        data = {"country": self.country_id, "type": "list"}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results']['type'], 'list')

    def test_filter_software(self):
        url = reverse("search-project-list")
        data = {"sw": "1"}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_innovation_categories(self):
        url = reverse("search-project-list")
        data = {"ic": "1"}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_filter_dhis(self):
        url = reverse("search-project-list")
        dhi_child = DigitalStrategy.objects.get(id=118)
        data = {"dhi": dhi_child.id}

        # Shouldn't find any, because we are filtering by parent categories only
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

        dhi_child = DigitalStrategy.objects.get(id=118)
        data = {"dhi": dhi_child.parent.id}

        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_filter_hfa(self):
        url = reverse("search-project-list")
        data = {"hfa": HealthFocusArea.objects.get(id=1).health_category.id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_filter_hsc(self):
        url = reverse("search-project-list")
        data = {"hsc": HSCChallenge.objects.get(id=1).id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_filter_bad_and_good_multi_filter_term(self):
        url = reverse("search-project-list")
        data = {"his": [1, 'k']}

        # will only search for the good filter term
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_filter_region(self):
        url = reverse("search-project-list")
        data = {"region": 0}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

        data = {"region": 1}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_filter_donor(self):
        url = reverse("search-project-list")
        data = {"donor": Donor.objects.all()[0].id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_filter_approved(self):
        url = reverse("search-project-list")
        data = {"approved": 1}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

        # there is no disapproved project at the moment, only one that is waiting for approval
        data = {"approved": 0}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

        self.project2.approval.approved = False
        self.project2.approval.save()

        data = {"approved": 0}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

        data = {"approved": 1}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_filter_view_as_donor_list_results_success(self):
        # add user to donor access
        self.d1.admins.add(self.userprofile)
        url = reverse("search-project-list")
        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "donor", "donor": self.d1.id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results']['type'], 'list')
        self.assertEqual(response.json()['results']['projects'][0]['donor_custom_answers'],
                         {str(self.d1.id): {}, str(self.d2.id): {}})
        self.assertEqual(response.json()['results']['projects'][0]['donor_custom_answers_private'],
                         {str(self.d1.id): {str(self.d1cq.id): ['answer1']}})

    def test_filter_view_as_country_list_results_success(self):
        # add user to country access
        self.country.admins.add(self.userprofile)

        url = reverse("search-project-list")
        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "country", "country": self.country_id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results']['projects'][0]['country_custom_answers'],
                         {})
        self.assertEqual(response.json()['results']['projects'][0]['country_custom_answers_private'],
                         {str(self.ccq1.id): ['answer country 1'], str(self.ccq2.id): ['answer country 2']})

    def test_search_view_as_donor_unsuccessful_flow(self):
        url = reverse("search-project-list")
        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "donor"}

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')

        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['No donor selected for view as.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "donor", "donor": self.d1.id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['No access to donor.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "donor", "donor": [self.d1.id, 999]}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['View as can only work with one donor selected.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "donor", "donor": [999]}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['No such donor.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "donor", "donor": 'aaa'}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['No such donor.'])

        self.d1.admins.add(self.userprofile)
        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "donor", "donor": self.d1.id}

        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_search_view_as_country_unsuccessful_flow(self):
        url = reverse("search-project-list")
        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "country"}
        self.country.admins.remove(self.userprofile)
        self.country.users.remove(self.userprofile)

        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')

        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['No country selected for view as.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "country", "country": self.country.id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['No access to country.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "country_lol", "country": self.country.id}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['You can only view as country or donor.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "country", "country": [self.country.id, 999]}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['View as can only work with one country selected.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "country", "country": [999]}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['No such country.'])

        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "country", "country": 'aaa'}
        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ['No such country.'])

        self.country.admins.add(self.userprofile)
        data = {"in": "name", "q": "phrase5", "type": "list", "view_as": "country", "country": self.country.id}

        response = self.test_user_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
