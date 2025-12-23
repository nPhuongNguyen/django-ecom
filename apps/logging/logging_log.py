import inspect
import json
import logging
import sys
import traceback
from django.conf import settings
from django.utils import timezone

from apps.config.kafka_config import PushO2mSmartlinkAPILog
from apps.utils import request_func
logger = logging.getLogger("o2m-smart-link-api-logging")

if not logger.handlers:
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def _log(level: str, message=None, **kwargs):
    _, _, exc_tb = sys.exc_info()
    def _short_caller(name, filename, lineno):
        file_short = '/'.join(filename.replace('\\','/').split('/')[-2:])
        return f"{name} | {file_short}:{lineno}"
    if exc_tb:
        tb_last = traceback.extract_tb(exc_tb)[-1]
        caller_info = _short_caller(tb_last.name, tb_last.filename, tb_last.lineno)
    else:
        frame = inspect.stack()[2]
        caller_info = _short_caller(frame.function, frame.filename, frame.lineno)
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_data = {
        "timestamp": timestamp,
        "level": level,
        "func_name": request_func.get_request_func(),
        "message": message,
        "caller": caller_info
    }
  
    if kwargs:
        log_data.update(kwargs)

    json_log = json.dumps(log_data, ensure_ascii=False)
    if settings.IS_DEV == 0:
        task = PushO2mSmartlinkAPILog(log_data)
        task.run()
    if exc_tb:
        log_data["stacktrace"] = traceback.format_exc()
        json_log = json.dumps(log_data, ensure_ascii=False)
    if level == "ERROR":
        logger.error(json_log)
    else:
        logger.info(json_log)

def log_info(message=None, **kwargs):
    _log("INFO", message, **kwargs)

def log_error(message=None, **kwargs):
    _log("ERROR", message, **kwargs)

