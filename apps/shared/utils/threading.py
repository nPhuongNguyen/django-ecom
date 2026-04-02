import threading
_thread_locals = threading.local()

class ThreadLocal:

    def set_request_id(request_id):
        return setattr(_thread_locals, "request_id", request_id)
    
    def get_request_id():
        return getattr(_thread_locals, "request_id", None)

    def clear_request_id():
        if hasattr(_thread_locals, "request_id"):
            del _thread_locals.request_id
    
    def set_request_func(func_name):
        return setattr(_thread_locals, "request_func", func_name)

    def get_request_func():
        return getattr(_thread_locals, "request_func", None)

    def clear_request_func():
        if hasattr(_thread_locals, "request_func"):
            del _thread_locals.request_func

