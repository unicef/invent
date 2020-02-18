from datetime import timedelta
from django.conf import settings
from django.utils import timezone

from celery.utils.log import get_task_logger

from core.utils import send_mail_wrapper
from project.models import Project
from toolkit.models import Toolkit
from scheduler.celery import app

logger = get_task_logger(__name__)


@app.task(name="send_daily_toolkit_digest")
def send_daily_toolkit_digest():
    """
    Sends daily digest on maps toolkit changes to team members.
    """
    projects = Project.objects.all()
    for project in projects:
        toolkit = Toolkit.objects.get_object_or_none(project_id=project.id)
        time_period = (timezone.localtime(timezone.now()) - timedelta(hours=settings.TOOLKIT_DIGEST_PERIOD))
        if toolkit and toolkit.modified > time_period:
            for profile in project.team.all():
                context = {"project_id": project.id}
                send_mail_wrapper(subject="Your Digital Health Atlas project has been updated",
                                  email_type="toolkit_digest",
                                  to=profile.user.email,
                                  language=profile.language,
                                  context=context)
