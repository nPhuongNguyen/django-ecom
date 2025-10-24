# yourapp/utils/get_request_id.py
import uuid

from apps.middleware.request_middleware import get_current_request

def get_request_id():
    request = get_current_request()
    if request is None:
        return str(uuid.uuid4())
    if not hasattr(request, "request_id"):
        request.request_id = str(uuid.uuid4())
    return request.request_id
