from core.data.review_questions import REVIEWER_QUESTIONS, MANAGER_QUESTIONS
from project.models import Portfolio, ProblemStatement, Project, ProjectPortfolioState
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
        self.pps.assign_questionnaire(self.user_1_profile)
        # prefill answers
        for question in self.user_1_profile.review_questions.all():
            if question.type == 'Select':
                question.choice_answer = 1
                question.save()

            elif question.type == 'SelectExtended':
                question.choice_answer = 1
                question.text_answer = 'test text'
                question.save()
            elif question.type == 'ProblemStatement':
                question.problem_statement.set([ProblemStatement.objects.get(name='PS 1')])

    def test_review_model_getters(self):
        self.assertEqual(len(self.user_1_profile.review_questions.all()), 8)
        attributes = {'name', 'text', 'guidance', 'type'}
        for attribute in attributes:
            expected_values = [x[attribute] for x in REVIEWER_QUESTIONS.values()]
            expected_values.sort()
            actual_values = [getattr(q, attribute) for q in self.user_1_profile.review_questions.all()]
            actual_values.sort()
            self.assertEqual(actual_values, expected_values)
        # check the remaining properties
        for question in self.user_1_profile.review_questions.all():
            answer = question.answer
            if question.type == 'Select':
                self.assertTrue(isinstance(answer, int))
                self.assertTrue(isinstance(question.choices, list))
            elif question.type == 'SelectExtended':
                self.assertTrue(isinstance(answer, tuple))
                self.assertTrue(isinstance(question.choices, list))
            elif question.type == 'ProblemStatement':
                self.assertFalse(isinstance(answer, int))
                self.assertFalse(isinstance(answer, tuple))
                self.assertTrue(question.choices is None)

    def test_portfolio_state_getters(self):
        self.assertEqual(self.pps.impact.name, MANAGER_QUESTIONS['m_i']['name'])
        self.assertEqual(self.pps.scale_phase.name, MANAGER_QUESTIONS['m_sp']['name'])
