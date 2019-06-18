from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings
from django.template import loader

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery # noqa


class Command(BaseCommand):
    help = """
    Sends HTML rendered template
    usage: send_html_email <type> <email address>
    eg: send_html_email email_confirmation_signup_message no@pulilab.com
    """

    def add_arguments(self, parser):
        parser.add_argument('type')
        parser.add_argument('email')
        parser.add_argument('--project-id', dest="project_id", required=False)
        parser.add_argument('--project-name', dest="project_name", required=False)
        parser.add_argument('--language', dest="language", required=False)
        parser.add_argument('--r', dest="role", required=False)
        parser.add_argument('--group', dest="group", required=False)
        parser.add_argument('--name', dest="name", required=False)
        parser.add_argument('--change-url', dest="change_url", required=False)
        parser.add_argument('--country-name', dest="country_name", required=False)
        parser.add_argument('--donor-name', dest="donor_name", required=False)
        parser.add_argument('--full-name', dest="full_name", required=False)
        parser.add_argument('--activate-url', dest="activate_url", required=False)

    def handle(self, *args, **options):
        excluded = {'settings', 'verbosity', 'pythonpath', 'traceback', 'no_color'}
        renderOptions = {x: options[x] for x in options if x not in excluded}
        self.stdout.write("-- Trying to send an email")
        self.stdout.write("-- Template filled with {}".format(renderOptions))
        email = options['email']
        html_template = loader.get_template("email/master-inline.html")
        html_message = html_template.render(renderOptions)
        send_mail(
            subject="Test HTML templates",
            message="",
            from_email=settings.FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message)

        self.stdout.write("-- Email sent to: %s" % email)
