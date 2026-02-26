import uuid
from apps.logging import logging_log as lg
from apps.logging.log_request import RequestLogger
import time
import uuid
from apps.logging import logging_log as lg
from apps.logging.log_request import RequestLogger
from ..utils.request_func import UtilsRequestFunc

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            start = time.perf_counter()
            request_func = (
                request.headers.get("X-Request-ID") or uuid.uuid4().hex
            )
            UtilsRequestFunc.init_request_func(request_func)
            request_info = RequestLogger.process_request(request)
            lg.log_info(
                request=request_info,
                message="[REQUEST][START]"
            )
            try:
                response = self.get_response(request)
            except Exception:
                end = time.perf_counter()
                duration_ms = (end - start) * 1000
                lg.log_error(
                    message="[EXCEPTION] Error",
                    duration_ms=duration_ms
                )
            end = time.perf_counter()
            duration_ms = (end - start) * 1000
            lg.log_info(
                message="[REQUEST][END]",
                duration_ms=duration_ms
            )
            return response
        finally:
            UtilsRequestFunc.clear_request_func()
