from django.db import models
from core.models import GetObjectOrNoneQueryset
from django.contrib.postgres.fields import JSONField


class LogBase(models.Model):
    """
    Basic properties and functions required by all Log models
    - date: Year and Month of the DB entry
    - data: JSONField. All KPI classes store data in a JSONField

    Data is updated each day by a celery task running after midnight
    """
    date = models.DateField(blank=False, help_text='WARNING: Only use the year and month of this', null=False)
    data = JSONField(blank=True, default=dict)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = GetObjectOrNoneQueryset.as_manager()

    class Meta:
        abstract = True


class SolutionLog(LogBase):
    """
    [
      {
        "date": "YYYY-MM",
        "data": {
          "portfolios": [
            {
              "id": "<portfolio_id>",
              "investment_to_date": 999999,
              "innovation_hub": true,
              "status": "DR",
              "problem_statements": [
                "<problem_statement_id>"
              ],
              "solutions": [
                "<solution_id>"
              ]
            }
          ],
          "solutions": [
            {
              "id": "<solution_id>",
              "people_reached": 99999,
              "phase": "<choice_int>",
              "regions": [
                "<choice_int>"
              ],
              "countries": [
                "<country_id>"
              ],
              "open_source_frontier_tech": true,
              "learning_investment": true,
              "problem_statements": [
                "<problem_statement_id>"
              ],
              "portfolios": [
                "<portfolio_id>"
              ]
            }
          ]
        }
      }
    ]
    """
    pass
