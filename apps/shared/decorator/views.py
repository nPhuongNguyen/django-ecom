from functools import wraps

def mask_view(**kwargs):
    accordion = kwargs.get('accordion', None)
    space_code = kwargs.get('space_code', None)
    def decorator(func_view):
        @wraps(func_view)
        def wrapper(self, request, *args, **kwargs):
            context = {
                'accordion': accordion,
                'space_code': space_code
            }
            return func_view(self, request, *args, context=context, **kwargs)
        return wrapper
    return decorator
