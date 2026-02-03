from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from apps.logging import logging_log as lg
class UtilsMail:
    @staticmethod
    def send(
        subject: str,
        to: list,
        message: str = '',
        html_message: str | None = None,
        from_email: str | None = None,
        fail_silently: bool = False
    ):
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email or settings.DEFAULT_FROM_EMAIL,
                recipient_list=to,
                html_message=html_message,
                fail_silently=fail_silently,
            )
            lg.log_info(
                message="[MAIL][SENT]",
                to=to,
                subject=subject
            )
        except Exception:
            lg.log_error(
                message="[MAIL][ERROR]"
            )
