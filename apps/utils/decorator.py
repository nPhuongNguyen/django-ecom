
from functools import wraps
from rest_framework import serializers
from apps.logging import logging as lg
from apps.shared.response import ResponseBuilder, ResponseCodes

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
                return ResponseBuilder.build(
                    code=ResponseCodes.INVALID_INPUT
                )
            if not serializer.is_valid():
                lg.log_info(
                    message=f"Serializer invalid: errors={serializer.errors}"
                )
                return ResponseBuilder.build(
                    code=ResponseCodes.INVALID_INPUT,
                    errors=serializer.errors
                )
            request.validated_data = serializer.validated_data
            lg.log_info(
                message=f"Serializer validated_data: {request.validated_data}"
            )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

