import json

from urllib3 import request
class RequestLogger:
    @staticmethod
    def process_request(request):
        method, path, remote_addr, content_type, data, files = RequestLogger.input_request(request)
        files_log = {
            k: {
                "filename": f.name,
                "size": f.size,
                "content_type": f.content_type
            }
            for k, f in files.items()
        } if files else {}
        request_info = {
            "method": method,
            "path": path,
            "remote_addr": remote_addr,
            "content_type": content_type,
            "data": data,
            "files": files_log
        }
        return request_info, files
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
        data_params = request.GET.dict()
        data_body = {}
        files = {}
        if "application/json" in content_type:
            try:
                data_body = json.loads(request.body.decode("utf-8"))
            except Exception:
                data_body = {}
        else:
            data_body = request.POST.dict()
            files = request.FILES
        data_input = {
            "params": data_params,
            "body": data_body
        }
        return method, path, remote_addr, content_type, data_input, files
        
