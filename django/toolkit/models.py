from statistics import mean

from django.db import models
from django.contrib.postgres.fields import JSONField

from core.models import ExtendedModel
from project.models import Project


class Toolkit(ExtendedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    data = JSONField()

    def update_score(self, axis, domain, question, answer, value):
        """
        Updates the scores of the given toolkit object, as follows:

            - Score for the answer
            - Question score sum
            - Domain score sum
            - Domain percentage
            - Axis score
            - Axis completion

        Args:
            axis: index of axis
            domain: index of domain inside axis
            question: index of question inside of domain
            answer: index of answer inside of question
            value: value to update the answer

        Raises:
            IndexError: if any index is out of range
        """
        # Save the new score to the answer.
        self.data[axis]["domains"][domain]["questions"][question]["answers"][answer] = value

        # Filter out -1 values from answers since those stand for not applicable.
        answers = self.data[axis]["domains"][domain]["questions"][question]["answers"]
        applicable_answers = list(filter(lambda x: x is None or x >= 0, answers))

        # Update the question score sum (sum of answers).
        self.data[axis]["domains"][domain]["questions"][question]["question_sum"] = sum(
            filter(None, applicable_answers))

        # Update the domain score sum (sum of question sums).
        questions = self.data[axis]["domains"][domain]["questions"]
        domain_sum = sum(x["question_sum"] for x in questions)
        self.data[axis]["domains"][domain]["domain_sum"] = domain_sum

        # Calculate non applicable points to reduce from question max.
        question_max = self.data[axis]["domains"][domain]["questions"][question]["question_max"]
        points_to_reduce_max = question_max / len(answers) * (len(answers) - len(applicable_answers))

        # Adjust the domain max with non applicable points for the calculation.
        domain_max = self.data[axis]["domains"][domain]["domain_max"] - points_to_reduce_max

        # Update the domain percentage (sum/max*100).
        domain_percentage = (domain_sum / domain_max) * 100
        self.data[axis]["domains"][domain]["domain_percentage"] = domain_percentage

        # Update the axis score (average of domain percentages).
        axis_score = mean([x["domain_percentage"] for x in self.data[axis]["domains"]])
        self.data[axis]["axis_score"] = axis_score

        # Update domain completion percentage
        all_domain_answers = [
            answer for questions in self.data[axis]["domains"][domain]["questions"] for answer in questions["answers"]
        ]
        answered_domain_answers = [
            answer for questions in self.data[axis]["domains"][domain]["questions"] for answer in questions["answers"]
            if answer is not None
        ]
        domain_completion = (len(answered_domain_answers) / len(all_domain_answers)) * 100
        self.data[axis]["domains"][domain]["domain_completion"] = domain_completion

        # Update the axis completion percentage.
        all_axis_answers = [
            answer
            for domains in self.data[axis]["domains"] for questions in domains["questions"]
            for answer in questions["answers"]
        ]
        answered_axis_answers = [
            answer
            for domains in self.data[axis]["domains"] for questions in domains["questions"]
            for answer in questions["answers"] if answer is not None
        ]
        axis_completion = (len(answered_axis_answers) / len(all_axis_answers)) * 100
        self.data[axis]["axis_completion"] = axis_completion

        self.save()


class ToolkitVersion(ExtendedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    version = models.IntegerField()
    data = JSONField()
