
from apps.middleware import request_middleware

def set_request_func(func_name):
    request_middleware.set_request_func(func_name)

def get_request_func():
    request_func = request_middleware.get_request_func()
    return request_func
