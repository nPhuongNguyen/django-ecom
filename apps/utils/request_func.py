
from ..shared.utils.contextvar import RequestContext

class UtilsRequestFunc:
    @staticmethod
    def set_request_id(request_id):
        return RequestContext.set_request_id(request_id)
    @staticmethod
    def get_request_id():
        return RequestContext.get_request_id()
    @staticmethod
    def set_request_func(func_name):
        return RequestContext.set_request_func(func_name)
    @staticmethod
    def get_request_func():
        return RequestContext.get_request_func()
    @staticmethod
    def clear_request_func():
        RequestContext.clear_request_func()
        RequestContext.clear_request_func()
