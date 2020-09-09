from project.models import Portfolio, Project, ProjectPortfolioState
from user.models import UserProfile
from project.tests.portfolio_tests import PortfolioSetup


class ReviewTests(PortfolioSetup):
    def setUp(self):
        super(ReviewTests, self).setUp()
        # User roles: User 1 (normal user), User 2 (global portfolio owner), User 3 (manager of portfolio 1)
        self.project = Project.objects.get(id=self.project_1_id)
        self.portfolio = Portfolio.objects.get(id=self.portfolio_id)
        self.pps = ProjectPortfolioState.objects.create(project=self.project, portfolio=self.portfolio)
        self.user_1_profile = UserProfile.objects.get(id=self.user_1_pr_id)

    def test_review_assign_questions(self):
        review, created = self.pps.assign_questionnaire(self.user_1_profile)
        self.assertTrue(created)
        self.assertIsNotNone(review)
        review_id = review.id
        review, created = self.pps.assign_questionnaire(self.user_1_profile)
        self.assertFalse(created)
        self.assertIsNotNone(review)
        self.assertEqual(review.id, review_id)
