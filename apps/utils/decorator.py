
from functools import wraps
from rest_framework import serializers
from apps.logging import logging as lg
from apps.shared.response import ResponseFormat

def catch_exceptions():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            lg.log_info(
                message=f"Input args: {args}, kwargs: {kwargs}"
            )
            try:
                result = func(*args, **kwargs)
                lg.log_info(
                    message=f"Return: {result}"
                )
                return result
            except Exception as e:  # pylint: disable=broad-exception-caught
                lg.log_error(
                    message=str(e)
                )
                return ResponseFormat.response_format(
                    status_code = 50040,
                    msg = "Hệ thống đang lỗi. Vui lòng thử lại sau!",
                    data = None
                )
        return wrapper
    return decorator

def validate_serializer(serializer_class : type[serializers.Serializer]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                serializer = serializer_class(data=request.data)
            except Exception as e:
                lg.log_error(
                    message=f"JSON parse error: {str(e)}"
                )
                return ResponseFormat.response_format(
                    status_code=40040,
                    msg="Dữ liệu không hợp lệ. Vui lòng kiểm tra lại!",
                    data=None
                )
            if not serializer.is_valid():
                lg.log_info(
                    message=f"Serializer invalid: errors={serializer.errors}"
                )
                return ResponseFormat.response_format(
                    status_code = 40040,
                    msg = "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại!",
                    data = None
                )
            request.validated_data = serializer.validated_data
            lg.log_info(
                message=f"Serializer validated_data: {request.validated_data}"
            )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

