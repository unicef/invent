from typing import Dict, Union, List
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import override, ugettext


def send_mail_wrapper(subject: str, email_type: str,
                      to: Union[str, List[str]], language: str,
                      context: Dict = None) -> None:
    if context is None:  # pragma: no cover
        context = {}

    html_template = loader.get_template("email/master-inline.html")
    context.update(
        {
            "type": email_type,
            "language": language,
            "email": to
        }
    )

    with override(language):
        html_message = html_template.render(context)
        subject = ugettext(subject)

        send_mail(
            subject=subject,
            message="",
            from_email=settings.FROM_EMAIL,
            recipient_list=[to] if type(to) == str else to,
            html_message=html_message)
