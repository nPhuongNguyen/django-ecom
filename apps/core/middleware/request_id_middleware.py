# yourapp/middleware/request_id_middleware.py
import uuid
import threading

_thread_locals = threading.local()

def get_current_request():
    """Lấy request hiện tại từ thread local"""
    return getattr(_thread_locals, "request", None)

class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # lưu request vào thread local
        _thread_locals.request = request

        # gán request_id nếu chưa có
        if not hasattr(request, "request_id"):
            request.request_id = str(uuid.uuid4())

        response = self.get_response(request)

        response["X-Request-ID"] = request.request_id
        return response
