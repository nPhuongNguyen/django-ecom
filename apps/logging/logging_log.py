
import json
import logging
import sys
from django.conf import settings
from django.utils import timezone

from apps.config.kafka_config import PushO2mSmartlinkAPILog
from apps.utils import request_func
logger = logging.getLogger("o2m-smart-link-api-logging")
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = json.loads(record.getMessage())
        format_caller = f"{record.funcName} | {record.filename}:{record.lineno}"
        log_data["caller"] = format_caller
        if record.exc_info:
            log_data["traceback"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)

if not logger.handlers:
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(JsonFormatter())
    logger.addHandler(ch)

def _log(level: str, message=None, **kwargs):
    log_data = {
        "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "level": level,
        "func_name": request_func.get_request_func(),
        "message": message,
    }

    if kwargs:
        log_data.update(kwargs)

    json_msg = json.dumps(log_data, ensure_ascii=False)
    has_exception = sys.exc_info()[0] is not None
    try:
        if level == "ERROR":
            logger.error(json_msg, stacklevel=3, exc_info=has_exception)
        else:
            logger.info(json_msg, stacklevel=3)
    finally:
        if settings.IS_DEV == 0:
            PushO2mSmartlinkAPILog(log_data).run()
def log_info(message=None, **kwargs):
    _log("INFO", message, **kwargs)

def log_error(message=None, **kwargs):
    _log("ERROR", message, **kwargs)

