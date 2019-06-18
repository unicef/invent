import logging

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from djcelery_email.backends import CeleryEmailBackend
from djcelery_email.utils import email_to_dict, chunked
from djcelery_email.tasks import send_emails


class ExceptionLoggingMiddleware(MiddlewareMixin):
    """
    This Middleware enables proper exception stacktrace logging under Gunicorn.
    """

    def process_exception(self, request, exception):  # pragma: no cover
        logging.exception('Exception handling request for ' + request.path)


class TestCeleryEmailBackend(CeleryEmailBackend):
    def send_messages(self, email_messages):  # pragma: no cover
        result_tasks = []
        for msg in email_messages:
            msg.to = settings.TEST_FORCED_TO_ADDRESS
            msg.cc = []
            msg.bcc = []
        messages = [email_to_dict(msg) for msg in email_messages]
        for chunk in chunked(messages, settings.CELERY_EMAIL_CHUNK_SIZE):
            result_tasks.append(send_emails.delay(chunk, self.init_kwargs))
        return result_tasks
