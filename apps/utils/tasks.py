

from celery import shared_task

from ..config.kafka_config import InitBroker

from .utils_mail import UtilsMail
import sys

@shared_task(
        bind=True,
        queue='woker-push-task',
    )
def send_mail_task(
    self,
    subject: str,
    to: list,
    message: str = '',
    html_message: str | None = None,
    from_email: str | None = None,
):
    try:
        UtilsMail.send(
            subject=subject,
            to=to,
            message=message,
            html_message=html_message,
            from_email=from_email,
        )
    except Exception as e:
        _retry = self.request.retries
        if _retry < 3:
            sys.stdout.write(f"Retry: {_retry + 1}/3\n[Mail Task] Error: {e} | Traceback: {sys.exc_info()}\n")
            raise self.retry()
        else:
            sys.stdout.write(f"Retry: 3/3\n[Mail Task] FAILED after 3 attempts. Giving up.\n")
            return

@shared_task(
    bind=True,
    queue='woker-push-task',
)
def push_kafka_task(self, key: str, message: dict):
    init_log_broker = InitBroker()
    try:
        init_log_broker.push_log_django_ecom.run(key=key, message=message)
        sys.stdout.write(f"Key: {key} | Message: {message}\nKafka log pushed successfully.\n")
    except Exception as e:
        _retry = self.request.retries
        if _retry < 3:
            sys.stdout.write(f"Retry: {_retry + 1}/3\nKey: {key} | Message: {message}\n[Kafka System Error] {e} | Traceback: {sys.exc_info()}\n")
            raise self.retry()
        else:
            sys.stdout.write(f"Retry: 3/3\nKey: {key} | Message: {message}\n[Kafka System Error] FAILED after 3 attempts. Giving up.\n")
            return