
from ..shared.utils.threading import ThreadLocal

class UtilsRequestFunc:
    def init_request_func(func_name):
        return ThreadLocal.init_request_func(func_name)

    def set_request_func(func_name):
        return ThreadLocal.set_request_func(func_name)

    def get_request_func():
        return ThreadLocal.get_request_func()

    def clear_request_func():
        return ThreadLocal.clear_request_func()