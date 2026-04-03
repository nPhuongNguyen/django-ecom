import logging
from django.conf import settings
from django.utils import timezone
import inspect
import os
from apps.utils.tasks import push_kafka_task
from ..utils.request_func import UtilsRequestFunc
logger = logging.getLogger("o2m-smart-link-api-logging")

def _log(level: str, message=None, **kwargs):
    try:
        caller_frame = inspect.stack()[2]
        caller_info = {
            "caller": f"{caller_frame.function} | {os.path.basename(caller_frame.filename)}:{caller_frame.lineno}"
        }
    except Exception:
        caller_info = {
            "caller": "Unknown Caller"
        }
    log_data = {
        "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "level": level,
        "request_id": UtilsRequestFunc.get_request_id(),
        "func_name": UtilsRequestFunc.get_request_func(),
        "message": message,
    }
    if kwargs:
        log_data.update(kwargs)
    log_data.update(caller_info)
    try:
        if level == "ERROR":
            logger.error(log_data)
        else:
            logger.info(log_data)
    finally:
        if settings.IS_DEV == 0:
            push_kafka_task.delay(
                key="django_ecom_log", 
                message=log_data
            )

def log_info(message=None, **kwargs):
    _log("INFO", message, **kwargs)

def log_error(message=None, **kwargs):
    _log("ERROR", message, **kwargs)

