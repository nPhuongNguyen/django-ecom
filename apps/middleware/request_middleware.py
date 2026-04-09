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
            UtilsRequestFunc.set_request_id(request_func)
            request_info, files = RequestLogger.process_request(request)
            request.data_input = request_info.get("data", {})
            request.files = files
            lg.log_info(
                request=request_info,
                message="[REQUEST][START]"
            )
            try:
                response = self.get_response(request)
            except Exception:
                end = time.perf_counter()
                duration = f"{(end - start): .3f} s"
                lg.log_error(
                    message="[EXCEPTION] Error",
                    duration=duration
                )
            end = time.perf_counter()
            duration = f"{(end - start): .3f} s"
            response_data = ""
            if hasattr(response, "data") and isinstance(response.data, dict):
                response_data = response.data
            lg.log_info(
                message="[REQUEST][END]",
                status_code=response.status_code,
                response=response_data,
                duration=duration
            )
            return response
        finally:
            UtilsRequestFunc.clear_request_func()
