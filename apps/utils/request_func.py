
from ..shared.utils.threading import ThreadLocal

class UtilsRequestFunc:
    @staticmethod
    def set_request_id(request_id):
        return ThreadLocal.set_request_id(request_id)
    @staticmethod
    def get_request_id():
        return ThreadLocal.get_request_id()
    @staticmethod
    def set_request_func(func_name):
        return ThreadLocal.set_request_func(func_name)
    @staticmethod
    def get_request_func():
        return ThreadLocal.get_request_func()
    @staticmethod
    def clear_request_func():
        ThreadLocal.clear_request_func()
        ThreadLocal.clear_request_func()
