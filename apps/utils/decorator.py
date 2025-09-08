
from functools import wraps

from django.db import connection
from rest_framework.response import Response
from rest_framework import serializers

from apps.logging import logging as lg
from apps.utils import get_request

# def catch_exceptions(func):
#     @wraps(func) # arguments = [], keyword arguments = {}
#     def wrapper(*args, **kwargs):
#         if len(args) > 1:
#             request = args[1]
#             if isinstance(request, rest_framework.request.Request):
#                 request_id = None
#                 if request:
#                     request_id = getattr(request, "request_id", str(uuid.uuid4()))
#                     setattr(request, "request_id", request_id)
#         func_name = f"{func.__module__}.{func.__qualname__}"
#         try:
#             result = func(*args, **kwargs)
#             return result
#         except Exception as e:
#             print(f"Error Exception Decorator Func {func_name}: ",str(e))
#     return wrapper
def catch_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_id = get_request.get_request_id()
        func_name = f"{func.__module__}.{func.__qualname__}"
        lg.log_info(
            request_id=request_id,
            func_name=func_name,
            message=f"Input args: {args}, kwargs: {kwargs}"
        )
        try:
            result = func(*args, **kwargs)
            lg.log_info(
                request_id=request_id,
                func_name=func_name,
                message=f"Return: {result}"
            )
            return result
        except Exception as e:  # pylint: disable=broad-exception-caught
            lg.log_info(
                request_id=request_id,
                func_name=func_name,
                message=str(e)
            )
            return None
    return wrapper

def validate_serializer(serializer_class : type[serializers.Serializer]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            serializer = serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "statusCode": 0,
                        "message": "Validation failed",
                        "data": serializer.errors
                    }
                )
            request.validated_data = serializer.validated_data
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
def log_sql(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_index = len(connection.queries)
        result = func(*args, **kwargs)
        new_queries = connection.queries[start_index:]
        for q in new_queries:
            lg.log_info(
                request_id=get_request.get_request_id(),
                func_name=f"{func.__module__}.{func.__qualname__}",
                message=f"[SQL] {q['sql']} | time: {q['time']}s"
            )
        return result
    return wrapper
