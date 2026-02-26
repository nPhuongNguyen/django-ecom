import threading
_thread_locals = threading.local()

class ThreadLocal:
    def set_request_func(func_name):
        current = getattr(_thread_locals, "request_func", "")
        _thread_locals.request_func = f"{current}-{func_name}" if current else func_name
        return _thread_locals.request_func

    def init_request_func(func_name):
        _thread_locals.request_func = func_name
        return _thread_locals.request_func

    def get_request_func():
        return getattr(_thread_locals, "request_func", None)

    def clear_request_func():
        if hasattr(_thread_locals, "request_func"):
            del _thread_locals.request_func
