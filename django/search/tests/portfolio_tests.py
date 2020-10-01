from django.urls import reverse
from project.tests.portfolio_tests import PortfolioSetup


class PortfolioSearchTests(PortfolioSetup):
    def setUp(self):
        super().setUp()

        self.project2_id, *_ = self.create_new_project(self.user_2_client)
        self.project3_id, *_ = self.create_new_project(self.user_2_client)
        self.project4_id, *_ = self.create_new_project(self.user_2_client)
        self.project5_id, *_ = self.create_new_project(self.user_2_client)
        
        response = self.create_portfolio("Test Portfolio 2", "Port-o-folio", [self.user_3_pr_id], self.user_2_client)
        self.assertEqual(response.status_code, 201, response.json())
        self.portfolio2_id = response.json()['id']
        
        # add Project 2, 4 to a Portfolio
        url = reverse("portfolio-project-add", kwargs={"pk": self.portfolio_id})
        request_data = {"project": [self.project2_id, self.project4_id]}
        response = self.user_2_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 201, response.json())

    def test_list_all_in_portfolio_for_detail_page(self):
        url = reverse("search-project-list")
        data = {"portfolio": self.portfolio_id, "type": "portfolio"}
        response = self.user_2_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results']['projects'][0]['id'], self.project2_id)
        self.assertEqual(response.json()['results']['projects'][0]['portfolio'], self.portfolio_id)
        self.assertEqual(response.json()['results']['projects'][1]['id'], self.project4_id)
        self.assertEqual(response.json()['results']['projects'][1]['portfolio'], self.portfolio_id)

    def test_multi_portfolio_filter_should_not_work(self):
        # add Project 3 to a Portfolio 2
        url = reverse("portfolio-project-add", kwargs={"pk": self.portfolio2_id})
        request_data = {"project": [self.project3_id]}
        response = self.user_2_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 201, response.json())

        # it only finds the last query param
        url = reverse("search-project-list")
        data = {"portfolio": [self.portfolio_id, self.portfolio2_id], "type": "portfolio"}
        response = self.user_2_client.get(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results']['projects'][0]['id'], self.project3_id)
        self.assertEqual(response.json()['results']['projects'][0]['portfolio'], self.portfolio2_id)
