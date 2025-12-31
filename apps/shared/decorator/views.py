from functools import wraps

def mask_view(**kwargs):
    accordion = kwargs.get('accordion', None)
    accordion_child = kwargs.get('accordion_child', None)
    space_code = kwargs.get('space_code', None)
    menu_item_show = kwargs.get('menu_item_show', None)
    def decorator(func_view):
        @wraps(func_view)
        def wrapper(self, request, *args, **kwargs):
            context = {
                'accordion': accordion,
                'accordion_child': accordion_child,
                'space_code': space_code,
                'menu_item_show': menu_item_show
            }
            return func_view(self, request, *args, context=context, **kwargs)
        return wrapper
    return decorator
