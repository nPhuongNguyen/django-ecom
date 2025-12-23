from functools import wraps
from rest_framework.response import Response
from rest_framework import serializers

from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.utils.utils_token import decode_token, normalize_token
from ecom.settings import TOKEN_SECRET_KEY

def validate_serializer(serializer_class : type[serializers.Serializer]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:           
                serializer = serializer_class(data=request.data)
            except Exception as e:
                format = ResponseCodes.INVALID_INPUT
                return ResponseBuilder.build(format, errors=str(e))
            if not serializer.is_valid():
                format = ResponseCodes.INVALID_INPUT
                return ResponseBuilder.build(format, errors=serializer.errors)
            request.validated_data = serializer.validated_data
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

def validate_exception():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                response = func(self, request, *args, **kwargs)
                return response 
            except Exception as e:
                format = ResponseCodes.SYSTEM_ERROR
                return ResponseBuilder.build(format, errors=str(e))
        return wrapper
    return decorator


def token_required():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if 'Token' in request.headers:
                token = request.headers["Token"]
                bearer_prefix = normalize_token(token)
                data, error_format = decode_token(bearer_prefix, TOKEN_SECRET_KEY)
                if error_format:
                    return ResponseBuilder.build(error_format)
                request.data_decode_token = data
                return func(self, request, *args, **kwargs)
            else:
                format = ResponseCodes.TOKEN_REQUIRED
                return ResponseBuilder.build(format)
        return wrapper
    return decorator


