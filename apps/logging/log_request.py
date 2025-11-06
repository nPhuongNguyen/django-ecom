import json
class RequestLogger:
    @staticmethod
    def process_request(request):
        try:
            body = request.body.decode("utf-8")
            if body:
                try:
                    body = json.loads(body)
                except Exception:
                    pass
            else:
                body = None
        except Exception as e:
            body = f"Cannot read body: {e}"

        return{
            "method": request.method,
            "path": request.get_full_path(),
            "remote_addr": RequestLogger._get_client_ip(request),
            "headers": dict(request.headers),
            "query_params": request.GET.dict(),
            "body": body,
        }
    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
