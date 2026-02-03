from celery import shared_task

from .utils_mail import UtilsMail

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 10})
def send_mail_task(
    subject: str,
    to: list,
    message: str = '',
    html_message: str | None = None,
    from_email: str | None = None,
):
    UtilsMail.send(
        subject=subject,
        to=to,
        message=message,
        html_message=html_message,
        from_email=from_email,
    )
