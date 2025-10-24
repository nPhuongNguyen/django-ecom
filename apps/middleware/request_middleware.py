# yourapp/middleware/request_id_middleware.py
import uuid
import threading
from datetime import datetime
from apps.logging import logging as lg
_thread_locals = threading.local()

def get_current_request():
    """Lấy request hiện tại từ thread local"""
    return getattr(_thread_locals, "request", None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # lưu request vào thread local
        _thread_locals.request = request

        # gán request_id nếu chưa có
        if not hasattr(request, "request_id"):
            request.request_id = str(uuid.uuid4())

        start_time = datetime.now().timestamp() * 1000
        response = self.get_response(request)
        server_duration = (datetime.now().timestamp() * 1000) - start_time
        lg.log_info(
            request_id=request.request_id,
            func_name="RequestMiddleware",
            message=f"[DURATION] {request.method} {request.get_full_path()} "
                    f"| time: {server_duration}ms"
        )

        response["X-Request-ID"] = request.request_id
        return response
