from project.models import Portfolio, Project, ProjectPortfolioState, ReviewScore
from user.models import UserProfile
from project.tests.portfolio_tests import PortfolioSetup
from django.urls import reverse


class ReviewTests(PortfolioSetup):
    def setUp(self):
        super(ReviewTests, self).setUp()
        # User roles: User 1 (normal user), User 2 (global portfolio owner), User 3 (manager of portfolio 1)
        self.project = Project.objects.get(id=self.project_1_id)
        self.portfolio = Portfolio.objects.get(id=self.portfolio_id)
        # add other project
        self.project_rev_id = self.create_project("Test Project in Inventory", self.org, self.country_office,
                                                  [self.d1, self.d2], self.user_1_client)
        # Move project to review phase
        url = reverse("portfolio-review-start", kwargs={"portfolio_id": self.portfolio_id})
        request_data = {"project": [self.project_rev_id]}
        response = self.user_3_client.post(url, request_data, format="json")
        # will fail because project is not in portfolio
        self.assertEqual(response.status_code, 400, response.json())
        # add project to portfolio
        url = reverse('portfolio-detailed', kwargs={"pk": self.portfolio_id})
        response = self.user_1_client.get(url)
        projects = response.json()['projects']
        projects.append(self.project_rev_id)

        url = reverse("portfolio-update", kwargs={"pk": self.portfolio_id})
        update_data = {'projects': projects}
        response = self.user_3_client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, 200)
        # Move project to review phase
        url = reverse("portfolio-review-start", kwargs={"portfolio_id": self.portfolio_id})
        request_data = {"project": [self.project_rev_id]}
        response = self.user_3_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 201, response.json())
        self.project_rev = Project.objects.get(id=self.project_rev_id)
        self.pps = ProjectPortfolioState.objects.get(portfolio=self.portfolio, project=self.project_rev)
        self.user_1_profile = UserProfile.objects.get(id=self.user_1_pr_id)

    def test_get_project_states(self):
        # Test 0: incorrect filter
        url = reverse("portfolio-project-list",
                      kwargs={"pk": self.portfolio_id, 'project_filter': 'wanna_ponies'})
        response = self.user_3_client.get(url, format="json")
        self.assertEqual(response.status_code, 400)
        # Test 1: inventory
        url = reverse("portfolio-project-list",
                      kwargs={"pk": self.portfolio_id, 'project_filter': 'inventory'})
        response = self.user_3_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp_data[0]['id'], self.project_1_id)
        self.assertEqual(resp_data[0]['review_states'], None)
        # Test 2: review
        url = reverse("portfolio-project-list",
                      kwargs={"pk": self.portfolio_id, 'project_filter': 'review'})
        response = self.user_3_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp_data[0]['id'], self.project_rev_id)
        self.assertEqual(resp_data[0]['review_states']['id'], self.pps.id)
        self.assertEqual(resp_data[0]['review_states']['review_scores'], [])  # no questionnaire sent yet
        # Test 3: complete
        url = reverse("portfolio-project-list",
                      kwargs={"pk": self.portfolio_id, 'project_filter': 'approved'})
        response = self.user_3_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertEqual(len(resp_data), 0)

    def test_review_assign_questions(self):
        url = reverse("portfolio-assign-questionnaire",
                      kwargs={"portfolio_id": self.portfolio_id, 'portfolio_review_id': self.pps.id})
        request_data = {'userprofile': self.user_1_profile.id}
        response = self.user_3_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 201)
        created = response.json()['created']
        modified = response.json()['modified']
        question_id = response.json()['id']
        # Try to do it again, expect failure
        response = self.user_3_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 409)
        # check that the same, unchanged object is returned
        self.assertEqual(response.json()['created'], created)
        self.assertEqual(response.json()['modified'], modified)
        url = reverse('review-score-modify', kwargs={'pk': question_id})
        response = self.user_3_client.delete(url, format="json")
        self.assertEqual(response.status_code, 204)
        # check if it was removed
        questions = ReviewScore.objects.filter(id=question_id)
        self.assertEqual(len(questions), 0)

    def test_review_fill_scores(self):
        # create questions
        url = reverse("portfolio-assign-questionnaire",
                      kwargs={"portfolio_id": self.portfolio_id, 'portfolio_review_id': self.pps.id})
        request_data = {'userprofile': self.user_1_profile.id}
        response = self.user_3_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 201)
        question_id = response.json()['id']
        partial_data = {
            'ee': 1,
            'ra': 5,
            'ra_comment': "I don't even know what I'm doing"
        }
        url = reverse('review-score-modify', kwargs={"pk": question_id})
        response = self.user_1_client.post(url, partial_data, format="json")
        self.assertEqual(response.status_code, 200)
        url = reverse('review-score-get', kwargs={"pk": question_id})
        response = self.user_1_client.get(url, format="json")
        resp_data = response.json()
        self.assertEqual(resp_data['ee'], 1)
        self.assertEqual(resp_data['ra'], 5)
        self.assertEqual(resp_data['ra_comment'], "I don't even know what I'm doing")
        faulty_data = {
            'nst': 7  # Not allowed value
        }
        url = reverse('review-score-modify', kwargs={"pk": question_id})
        response = self.user_1_client.post(url, faulty_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['nst'], ['"7" is not a valid choice.'])
