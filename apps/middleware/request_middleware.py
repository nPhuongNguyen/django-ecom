import json
import uuid
import threading
from datetime import datetime
from apps.logging import logging_log as lg
from apps.logging.log_request import RequestLogger
_thread_locals = threading.local()


def set_request_func(func_name):
    _thread_locals.request_func = f"{func_name}-{_thread_locals.request_func}"

def get_request_func():
    return getattr(_thread_locals, "request_func", None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request_func = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        start_time = datetime.now().timestamp() * 1000
        request_data = RequestLogger.process_request(request)
        lg.log_info(
            message="[CALL]",
            request=request_data
        )
        response = self.get_response(request)
        duration = (datetime.now().timestamp() * 1000) - start_time
        try:
            body = response.content.decode("utf-8")
            if body:
                try:
                    body = json.loads(body)
                except Exception:
                    pass
            else:
                body = None
        except Exception as e:
            body = f"Cannot read response body: {e}"

        response_data = {
            "status": response.status_code,
            "headers": dict(response.items()),
            "body": body,
        }
        lg.log_info(
            message=f"[RESPONSE] | Duration: {duration:.2f} ms",
            response=response_data,
        )
        return response