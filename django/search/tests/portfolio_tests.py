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

