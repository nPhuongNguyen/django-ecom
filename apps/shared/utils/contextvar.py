from contextvars import ContextVar

_request_id = ContextVar("request_id", default=None)
_request_func = ContextVar("request_func", default=None)

class RequestContext:

    @staticmethod
    def set_request_id(request_id):
        _request_id.set(request_id)

    @staticmethod
    def get_request_id():
        return _request_id.get()

    @staticmethod
    def clear_request_id():
        _request_id.set(None)

    @staticmethod
    def set_request_func(func_name):
        _request_func.set(func_name)

    @staticmethod
    def get_request_func():
        return _request_func.get()

    @staticmethod
    def clear_request_func():
        _request_func.set(None)