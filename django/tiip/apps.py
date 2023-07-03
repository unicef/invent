from django.apps import AppConfig


# Up until Django 2.x, there was no explicit validation for app labels. 
# However, in newer versions, Django has introduced explicit validation 
# for app labels to conform to the rules of Python identifiers. 
# This caused an issue with the simple-feedback module not being able to 
# install so we added this to resolve this issue.
class SimpleFeedbackConfig(AppConfig):
    name = 'simple-feedback'
    label = 'simple_feedback'
