import json
import uuid
import threading
from datetime import datetime
from django.utils import timezone
from apps.logging import logging_log as lg
from apps.logging.log_request import RequestLogger
_thread_locals = threading.local()


def set_request_func(func_name):
    current = getattr(_thread_locals, "request_func", "")
    _thread_locals.request_func = f"{current}-{func_name}" if current else func_name

def get_request_func():
    return getattr(_thread_locals, "request_func", None)

def clear_request_func():
    if hasattr(_thread_locals, "request_func"):
        del _thread_locals.request_func

import json
import uuid
import threading
import time
from apps.logging import logging_log as lg
from apps.logging.log_request import RequestLogger

_thread_locals = threading.local()


def clear_request_func():
    if hasattr(_thread_locals, "request_func"):
        del _thread_locals.request_func


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request_func = (
            request.headers.get("X-Request-ID") or uuid.uuid4().hex
        )

        start = time.perf_counter()

        lg.log_info(
            message="[CALL]",
            request=RequestLogger.process_request(request),
        )

        try:
            response = self.get_response(request)
        except Exception as e:
            duration_ms = (time.perf_counter() - start) * 1000
            lg.log_error(
                message=f"[EXCEPTION] | Duration: {duration_ms:.2f} ms",
                error=str(e),
            )
            raise
        finally:
            clear_request_func()

        duration_ms = (time.perf_counter() - start) * 1000

        content_type = response.get("Content-Type", "")
        body = None

        if "application/json" in content_type:
            try:
                body = json.loads(response.content.decode("utf-8"))
            except Exception:
                body = "<INVALID JSON>"
        else:
            body = f"<{content_type}>"

        lg.log_info(
            message=f"[RESPONSE] | Duration: {duration_ms:.2f} ms",
            response={
                "status": response.status_code,
                "content_type": content_type,
                "body": body,
            },
        )

        return response
