from functools import wraps
from apps.logging import logging_log as lg
from rest_framework import serializers

from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.utils.utils_token import decode_token, normalize_token
from ecom.settings import TOKEN_SECRET_KEY

def validate_serializer(serializer_class: type[serializers.Serializer]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            lg.log_info(
                message="[VALIDATE_SERIALIZER][CALL]",
                view=self.__class__.__name__,
                func=func.__name__,
                serializer=serializer_class.__name__,
                input=request.data
            )

            try:
                serializer = serializer_class(data=request.data)
            except Exception as e:
                lg.log_error(
                    message="[VALIDATE_SERIALIZER][INIT_FAILED]",
                    view=self.__class__.__name__,
                    func=func.__name__,
                    serializer=serializer_class.__name__,
                    error=str(e)
                )
                return ResponseBuilder.build(
                    ResponseCodes.INVALID_INPUT,
                    errors=str(e)
                )

            if not serializer.is_valid():
                lg.log_error(
                    message="[VALIDATE_SERIALIZER][INVALID]",
                    view=self.__class__.__name__,
                    func=func.__name__,
                    serializer=serializer_class.__name__,
                    errors=serializer.errors
                )
                return ResponseBuilder.build(
                    ResponseCodes.INVALID_INPUT,
                    errors=serializer.errors
                )

            lg.log_info(
                message="[VALIDATE_SERIALIZER][SUCCESS]",
                view=self.__class__.__name__,
                func=func.__name__,
                serializer=serializer_class.__name__,
            )

            request.validated_data = serializer.validated_data
            return func(self, request, *args, **kwargs)

        return wrapper
    return decorator

def validate_exception():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                return func(self, request, *args, **kwargs)
            except Exception as e:
                lg.log_error(
                    message="[EXCEPTION][UNHANDLED]",
                    view=self.__class__.__name__,
                    func=func.__name__,
                    error=str(e),
                    input=getattr(request, "data", None),
                )
                return ResponseBuilder.build(
                    ResponseCodes.SYSTEM_ERROR,
                    errors=str(e)
                )
        return wrapper
    return decorator


def token_required():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):

            lg.log_info(
                message="[TOKEN][CALL]",
                view=self.__class__.__name__,
                func=func.__name__,
                headers=dict(request.headers)
            )
            if 'Token' not in request.headers:
                lg.log_error(
                    message="[TOKEN][MISSING]",
                    view=self.__class__.__name__,
                    func=func.__name__,
                )
                return ResponseBuilder.build(
                    ResponseCodes.TOKEN_REQUIRED
                )

            token = request.headers["Token"]

            try:
                bearer_prefix = normalize_token(token)
                data, error_format = decode_token(
                    bearer_prefix,
                    TOKEN_SECRET_KEY
                )
            except Exception as e:
                lg.log_error(
                    message="[TOKEN][DECODE_EXCEPTION]",
                    view=self.__class__.__name__,
                    func=func.__name__,
                    error=str(e)
                )
                return ResponseBuilder.build(
                    ResponseCodes.SYSTEM_ERROR
                )

            if error_format:
                lg.log_error(
                    message="[TOKEN][INVALID]",
                    view=self.__class__.__name__,
                    func=func.__name__,
                    error_code=error_format
                )
                return ResponseBuilder.build(error_format)
            
            lg.log_info(
                message="[TOKEN][SUCCESS]",
                view=self.__class__.__name__,
                func=func.__name__,
                data=data
            )

            request.data_decode_token = data
            return func(self, request, *args, **kwargs)

        return wrapper
    return decorator



