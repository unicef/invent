from project.models import Portfolio, Project, ProjectPortfolioState, ReviewScore, ProblemStatement
from user.models import UserProfile
from project.tests.portfolio_tests import PortfolioSetup
from django.urls import reverse
from random import randint


class ReviewTests(PortfolioSetup):
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

        portfolio = Portfolio.objects.get(id=self.portfolio_id)
        pps_data = portfolio.review_states.all()
        self.assertEqual(len(pps_data), 1)
        self.assertEqual(pps_data[0].project.id, self.project_rev_id)
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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'impact': ['"6" is not a valid choice.']})

        review_data_complete = {
            'psa': [ProblemStatement.objects.get(name="PS 1").id],
            'rnci': 2,
            'ratp': 4,
            'ra': 5,
            'ee': 5,
            'nst': 5,
            'nc': 5,
            'ps': 5,
            'impact': 5,
            'scale_phase': 6
        }
        response = self.user_3_client.post(url, review_data_complete, format="json")
        self.assertEqual(response.status_code, 200)
        self.pps.refresh_from_db()
        self.assertEqual(self.pps.reviewed, True)
        self.assertEqual(self.pps.approved, False)

        # Edit the official review of the project
        review_data_complete['nc'] = 4
        response = self.user_3_client.post(url, review_data_complete, format="json")
        self.assertEqual(response.status_code, 200)
        self.pps.refresh_from_db()
        self.assertEqual(self.pps.nc, 4)
        self.assertEqual(self.pps.reviewed, True)
        self.assertEqual(self.pps.approved, False)

        # now reviewed, approve project
        url = reverse('portfolio-project-approve', kwargs={'pk': self.portfolio_id})
        project_data = {'project': [self.project_rev_id]}
        response = self.user_3_client.post(url, project_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.pps.refresh_from_db()
        self.assertEqual(self.pps.approved, True)
        # try to modify the approved project
        url = reverse('portfolio-project-manager-review', kwargs={'pk': self.pps.id})
        review_data_complete['nc'] = 3
        response = self.user_3_client.post(url, review_data_complete, format="json")
        self.assertEqual(response.status_code, 403)
        self.pps.refresh_from_db()
        self.assertEqual(self.pps.nc, 4)
        self.assertEqual(self.pps.reviewed, True)
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
        pps_ids = {x['id'] for x in pps_data}
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
        pps = ProjectPortfolioState.all_objects.get(project_id=project_id)
        self.assertEqual(pps.is_active, False)
        pps_data = response.json()['review_states']
        self.assertEqual(len(pps_data), 1)
        self.assertEqual(pps_data[0]['project'], self.project_rev_id)
        # Re-add the project review to the portfolio
        url = reverse('portfolio-project-add', kwargs={'pk': self.portfolio_id})
        response = self.user_3_client.post(url, {'project': [project_id]}, format="json")
        self.assertEqual(response.status_code, 201)
        pps_ids_2 = {x['id'] for x in response.json()['review_states']}
        self.assertEqual(pps_ids_2, pps_ids)

    def test_portfolio_matrix_output(self):
        """
        - Create 5 projects for the portfolio
        - Move 4 of them to review w. different scores and problem statements,
        - Query the detailed results
        - Check if the matrix blobs are correct
        """
        # create new portfolio
        response = self.create_portfolio('Matrix test portfolio', "Portfolio for testing matrix output",
                                         [self.user_3_pr_id], self.user_2_client)
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
                'status': ReviewScore.STATUS_COMPLETE,
            }
            self.review_and_approve_project(pps, scores, self.user_2_client)
            i += 1

        portfolio = Portfolio.objects.get(id=portfolio_id)
        impact_data = portfolio.get_risk_impact_matrix()
        ambition_data = portfolio.get_ambition_matrix()
        self.assertEqual(len(impact_data), 2)
        self.assertEqual(len(ambition_data), 2)
        impact_ratios = {x['ratio'] for x in impact_data}
        ambition_ratios = {x['ratio'] for x in ambition_data}
        self.assertEqual(impact_ratios, {0.67, 1.0})
        self.assertEqual(ambition_ratios, {0.67, 1.0})
        problem_statement_matrix = portfolio.get_problem_statement_matrix()

        self.assertEqual(len(problem_statement_matrix['high_activity']), 0)
        self.assertEqual(len(problem_statement_matrix['moderate']), 5)
        self.assertEqual(len(problem_statement_matrix['neglected']), 2)
