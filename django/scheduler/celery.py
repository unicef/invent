import os

from celery import Celery

from django.conf import settings

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tiip.settings")

# Initialize the Celery app
app = Celery("scheduler", set_as_current=True)

# Load Celery settings from the Django settings file
app.config_from_object("django.conf:settings")

# Auto-discover tasks in all Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
