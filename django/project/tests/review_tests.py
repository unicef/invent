from project.models import Portfolio, Project, ProjectPortfolioState, ReviewScore, ProblemStatement
from user.models import UserProfile
from project.tests.portfolio_tests import PortfolioSetup
from django.urls import reverse
from random import randint


class ReviewTests(PortfolioSetup):

    @staticmethod
    def get_portfolio_data(portfolio_id, client):
        url = reverse('portfolio-detailed',
                      kwargs={"pk": portfolio_id})
        return client.get(url).json()

    def move_project_to_portfolio(self, portfolio_id, project_id, expected_response_status=201, client=None):
        if client is None:
            client = self.user_3_client
        url = reverse("portfolio-project-add", kwargs={"pk": portfolio_id})
        request_data = {"project": [project_id]}

        # check permissions with user_1_client, which is not allowed
        response = client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, expected_response_status, response.json())
        return response.json()

    def review_and_approve_project(self, pps, scores, client=None):
        if client is None:
            client = self.user_3_client  # pragma: no cover
        url = reverse('portfolio-project-manager-review', kwargs={'pk': pps.id})
        response = client.post(url, scores, format="json")
        self.assertEqual(response.status_code, 200, f'{response.json()}')

        project_id = pps.project.id

        url = reverse('portfolio-project-approve', kwargs={'pk': pps.portfolio.id})
        response = self.user_3_client.post(url, {'project': [project_id]}, format="json")
        self.assertEqual(response.status_code, 200, f'{response.json()}')
        return response.json()

    def setUp(self):
        super(ReviewTests, self).setUp()
        # User roles: User 1 (normal user), User 2 (global portfolio owner), User 3 (manager of portfolio 1)
        self.project = Project.objects.get(id=self.project_1_id)
        self.portfolio = Portfolio.objects.get(id=self.portfolio_id)
        # add other project
        self.project_rev_id, project_data, org, country, country_office, d1, d2 = \
            self.create_new_project(self.user_1_client)

        # Add project to portfolio
        # check permissions with user_1_client, which is not allowed
        self.move_project_to_portfolio(self.portfolio_id, self.project_rev_id, 403, self.user_1_client)
        # do it with user 3, who is a GPO
        response_json = self.move_project_to_portfolio(self.portfolio_id, self.project_rev_id, 201, self.user_3_client)
        pps_data = response_json['review_states']
        self.assertEqual(len(pps_data), 1)
        self.assertEqual(pps_data[0]['project'], self.project_rev_id)

        self.project_rev = Project.objects.get(id=self.project_rev_id)
        self.pps = ProjectPortfolioState.objects.get(portfolio=self.portfolio, project=self.project_rev)
        self.user_1_profile = UserProfile.objects.get(id=self.user_1_pr_id)

    def test_project_in_portfolio_status_changes(self):
        project_id, project_data, org, country, country_office, d1, d2 = \
            self.create_new_project(self.user_1_client)

        portfolio_data = self.get_portfolio_data(portfolio_id=self.portfolio_id, client=self.user_3_client)
        pps_data = portfolio_data['review_states']
        self.assertEqual(len(pps_data), 1)
        self.assertEqual(pps_data[0]['project'], self.project_rev_id)
        # Moving project from inventory to review state
        # Try the API with incorrect data
        url = reverse('portfolio-project-add', kwargs={'pk': self.portfolio_id})
        response = self.user_3_client.post(url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        response = self.user_3_client.post(url, {'project': []}, format="json")
        self.assertEqual(response.status_code, 400)
        response = self.user_3_client.post(url, {'project': [25000]}, format="json")
        self.assertEqual(response.status_code, 400)
        # do it the right way
        pps_data = self.move_project_to_portfolio(self.portfolio_id, project_id, 201)['review_states']
        self.assertEqual(len(pps_data), 2)
        # Moving project from review to approved state
        # Try to approve project without official manager review
        url = reverse('portfolio-project-approve', kwargs={'pk': self.portfolio_id})
        project_data = {'project': [self.project_rev_id]}
        response = self.user_3_client.post(url, project_data, format="json")
        self.assertEqual(response.status_code, 400)
        # Try to review portfolio as user 1 (not a GPO or manager)
        url = reverse('portfolio-project-manager-review', kwargs={'pk': self.pps.id})
        response = self.user_1_client.post(url, {}, format="json")
        self.assertEqual(response.status_code, 403)
        # try to review portfolio as user 3 portfolio manager
        review_data_incomplete = {
            # missing scale phase and impact
            'psa': [ProblemStatement.objects.get(name="PS 1").id],
            'rnci': 2,
            'ratp': 4,
            'ra': 5,
            'ee': 5,
            'nst': 5,
            'nc': 5,
            'ps': 5
        }
        response = self.user_3_client.post(url, review_data_incomplete, format="json")
        self.assertEqual(response.status_code, 400)
        expected_errors = {'impact': ['This field is required.'], 'scale_phase': ['This field is required.']}
        self.assertEqual(response.json(), expected_errors)
        review_data_complete = {
            'psa': [ProblemStatement.objects.get(name="PS 1").id],
            'rnci': 2,
            'ratp': 4,
            'ra': 5,
            'ee': 5,
            'nst': 5,
            'nc': 5,
            'ps': 5,
            'impact': 6,
            'scale_phase': 5
        }
        response = self.user_3_client.post(url, review_data_complete, format="json")
        self.assertEqual(response.status_code, 200)
        self.pps.refresh_from_db()
        self.assertEqual(self.pps.reviewed, True)
        self.assertEqual(self.pps.approved, False)
        # now reviewed, approve project
        url = reverse('portfolio-project-approve', kwargs={'pk': self.portfolio_id})
        project_data = {'project': [self.project_rev_id]}
        response = self.user_3_client.post(url, project_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.pps.refresh_from_db()
        self.assertEqual(self.pps.approved, True)

        # Moving project from approved to review state
        url = reverse('portfolio-project-disapprove', kwargs={'pk': self.portfolio_id})
        project_data = {'project': [self.project_rev_id]}
        response = self.user_3_client.post(url, project_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.pps.refresh_from_db()
        self.assertEqual(self.pps.approved, False)

        # Moving project from review state to inventory
        # Try the API with incorrect data
        pps_projects = {x['project'] for x in pps_data}
        self.assertEqual(pps_projects, {self.project_rev_id, project_id})
        url = reverse('portfolio-project-remove', kwargs={'pk': self.portfolio_id})
        response = self.user_3_client.post(url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        response = self.user_3_client.post(url, {'project': []}, format="json")
        self.assertEqual(response.status_code, 400)
        response = self.user_3_client.post(url, {'project': [25000]}, format="json")
        self.assertEqual(response.status_code, 400)
        response = self.user_3_client.post(url, {'project': [project_id]}, format="json")
        self.assertEqual(response.status_code, 200, response.json())
        pps_data = response.json()['review_states']
        self.assertEqual(len(pps_data), 1)
        self.assertEqual(pps_data[0]['project'], self.project_rev_id)

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
        self.assertEqual(resp_data['count'], 1)
        self.assertEqual(resp_data['results'][0]['id'], self.project_1_id)
        self.assertEqual(resp_data['results'][0]['review_states'], None)
        # Test 2: review
        url = reverse("portfolio-project-list",
                      kwargs={"pk": self.portfolio_id, 'project_filter': 'review'})
        response = self.user_3_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertEqual(resp_data['count'], 1)
        self.assertEqual(resp_data['results'][0]['id'], self.project_rev_id)
        self.assertEqual(resp_data['results'][0]['review_states']['id'], self.pps.id)
        self.assertEqual(resp_data['results'][0]['review_states']['review_scores'], [])  # no questionnaire sent yet
        # Test 3: complete
        url = reverse("portfolio-project-list",
                      kwargs={"pk": self.portfolio_id, 'project_filter': 'approved'})
        response = self.user_3_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertEqual(resp_data['count'], 0)

    def test_review_assign_questions(self):
        url = reverse("portfolio-assign-questionnaire",
                      kwargs={"portfolio_id": self.portfolio_id, 'project_id': self.project_rev.id})
        request_data = {'userprofile': [self.user_1_profile.id]}
        response = self.user_3_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        created = response.json()[0]['created']
        modified = response.json()[0]['modified']
        question_id = response.json()[0]['id']
        # Try to do it again
        response = self.user_3_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 200)
        # check that the same, unchanged object is returned
        self.assertEqual(response.json()[0]['id'], question_id)
        self.assertEqual(response.json()[0]['created'], created)
        self.assertEqual(response.json()[0]['modified'], modified)
        url = reverse('review-score-get-or-delete', kwargs={'pk': question_id})
        response = self.user_3_client.delete(url, format="json")
        self.assertEqual(response.status_code, 204)
        # check if it was removed
        questions = ReviewScore.objects.filter(id=question_id)
        self.assertEqual(len(questions), 0)

    def test_review_fill_scores(self):
        # create questions
        url = reverse("portfolio-assign-questionnaire",
                      kwargs={"portfolio_id": self.portfolio_id, 'project_id': self.project_rev_id})
        request_data = {'userprofile': [self.user_1_profile.id]}
        response = self.user_3_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 200)

        question_id = response.json()[0]['id']
        pps_id = response.json()[0]['portfolio_review']
        # create a new user who is not associated with the review or the portfolio in any way
        user_x_pr_id, user_x_client, user_x_key = self.create_user('donkey@kong.com', '12345789TIZ', '12345789TIZ')
        partial_data = {
            'ee': 1,
            'ra': 5,
            'nst_comment': 'I do not know how to set this'
        }
        url = reverse('review-score-fill', kwargs={"pk": question_id})
        # Try to fill the answers with the unauthorized user
        response = user_x_client.post(url, partial_data, format="json")
        self.assertEqual(response.status_code, 403)  # UNAUTHORIZED
        # try to fill in faulty data - should not be allowed
        faulty_data = {
            'nst': 7  # Not allowed value
        }
        url = reverse('review-score-fill', kwargs={"pk": question_id})
        response = self.user_1_client.post(url, faulty_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['nst'], ['"7" is not a valid choice.'])

        response = self.user_1_client.post(url, partial_data, format="json")
        self.assertEqual(response.status_code, 200)

        # add another user review
        user_y_pr_id, user_y_client, user_y_key = self.create_user('jeff@bezos.com', '12345789TIZ', '12345789TIZ')
        url = reverse("portfolio-assign-questionnaire",
                      kwargs={"portfolio_id": self.portfolio_id, 'project_id': self.project_rev_id})
        request_data = {'userprofile': [user_y_pr_id]}
        response = self.user_3_client.post(url, request_data, format="json")
        self.assertEqual(response.status_code, 200)
        question_id_y = response.json()[0]['id']

        partial_data_2 = {
            'ee': 2,
            'ra': 4,
            'nst': 1,
            'nst_comment': 'Neither do I'
        }
        url = reverse('review-score-fill', kwargs={"pk": question_id_y})
        response = user_y_client.post(url, partial_data_2, format="json")
        self.assertEqual(response.status_code, 200)

        # read pps data
        url = reverse('portfolio-project-manager-review', kwargs={'pk': pps_id})
        response = self.user_1_client.get(url, {}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['averages']['ee'], 1.5)
        self.assertEqual(response.json()['averages']['ra'], 4.5)
        self.assertEqual(response.json()['averages']['nst'], 1.0)
        self.assertEqual(response.json()['averages']['rnci'], None)
        self.assertEqual(len(response.json()['review_scores']), 2)

        # Try to modify the answers - should not be allowed
        partial_data = {
            'rnci_comment': "I always forget this!",
        }
        response = self.user_1_client.post(url, partial_data, format="json")
        self.assertEqual(response.status_code, 403)  # UNAUTHORIZED
        url = reverse('review-score-get-or-delete', kwargs={"pk": question_id})
        response = self.user_1_client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertEqual(resp_data['ee'], 1)
        self.assertEqual(resp_data['ra'], 5)
        self.assertEqual(resp_data['rnci_comment'], None)

    def test_portfolio_matrix_output(self):
        """
        - Create 5 projects for the portfolio
        - Move 4 of them to review w. different scores and problem statements,
        - Query the detailed results
        - Check if the matrix blobs are correct
        """
        # create new portfolio
        response = self.create_portfolio('Matrix test portfolio', "Portfolio for testing matrix output",
                                         [self.user_3_pr_id],  self.user_2_client)
        self.assertEqual(response.status_code, 201, response.json())
        portfolio_id = response.json()['id']
        project_ids = list()
        for _ in range(5):
            project_id = self.create_new_project(self.user_2_client)[0]
            project_ids.append(project_id)
            self.move_project_to_portfolio(portfolio_id, project_id)
        pps_list = Portfolio.objects.get(id=portfolio_id).review_states.all()
        problem_statements = list()
        for i in range(5):
            problem_statements.append(ProblemStatement.objects.create(
                name=f"PS_Portfolio_{i}", description=f"PS_{i} description",
                portfolio=Portfolio.objects.get(id=portfolio_id)))

        i = 0
        for pps in pps_list:
            psa_current = [problem_statements[j].pk for j in range(0, 5, i % 2 + 1)]

            scores = {
                'psa': psa_current,
                'rnci': randint(1, 5),
                'ratp': randint(1, 5),
                'ra': i % 2 + 1,
                'ee': randint(1, 5),
                'nst': i % 2 + 1,
                'nc': i % 2 + 1,
                'ps': randint(1, 5),
                'impact': i % 2 + 1,
                'scale_phase': randint(1, 5),
            }
            self.review_and_approve_project(pps, scores, self.user_2_client)
            i += 1

        portfolio_details = self.get_portfolio_data(portfolio_id, self.user_2_client)
        impact_data = portfolio_details['risk_impact_matrix']
        ambition_data = portfolio_details['ambition_matrix']
        self.assertEqual(len(impact_data), 2)
        self.assertEqual(len(ambition_data), 2)
        impact_ratios = {x['ratio'] for x in impact_data}
        ambition_ratios = {x['ratio'] for x in ambition_data}
        self.assertEqual(impact_ratios, {0.67, 1.0})
        self.assertEqual(ambition_ratios, {0.67, 1.0})
        problem_statement_matrix = portfolio_details['problem_statement_matrix']

        self.assertEqual(len(problem_statement_matrix['high_activity']), 0)
        self.assertEqual(len(problem_statement_matrix['moderate']), 3)
        self.assertEqual(len(problem_statement_matrix['neglected']), 4)
