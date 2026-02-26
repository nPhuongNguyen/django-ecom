import json

from urllib3 import request
class RequestLogger:
    @staticmethod
    def process_request(request):
        method, path, remote_addr, content_type, data = RequestLogger.input_request(request)
        return{
            "method": method,
            "path": path,
            "remote_addr": remote_addr,
            "content_type": content_type,
            "data": data
        }
    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
    @staticmethod
    def input_request(request):
        content_type = request.headers.get("Content-Type", "")
        path = request.get_full_path()
        remote_addr = RequestLogger._get_client_ip(request)
        method = request.method.upper()
        data_input = None
        if method in ("GET", "DELETE"):
            data_input = request.GET.dict()
        elif method in ("POST", "PUT", "PATCH"):
            if "application/json" in content_type:
                try:
                    raw = request.body
                    data_input = json.loads(raw.decode("utf-8"))
                except Exception:
                    data_input = "<INVALID JSON>"
            else:
                data_input = f"<SKIP {content_type}>"
        return method, path, remote_addr, content_type, data_input
        
