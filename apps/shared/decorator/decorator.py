from functools import wraps
import time

from ...logging.log_request import RequestLogger
from ...config.redis_config import RedisService
from apps.logging import logging_log as lg
from rest_framework import serializers

from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.utils.utils_token import decode_token, normalize_token
from ecom.settings import TOKEN_SECRET_KEY
from apps.catalogue.serializers.token import InfoTokenSerializer

def validate_serializer(serializer_class: type[serializers.Serializer]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            lg.log_info(
                message="[VALIDATE_SERIALIZER][CALL]",
                input=request.data
            )

            try:
                serializer = serializer_class(data=request.data)
            except Exception as e:
                lg.log_error(
                    message="[VALIDATE_SERIALIZER][INIT_FAILED]"
                )
                return ResponseBuilder.build(
                    ResponseCodes.INVALID_INPUT,
                    errors=str(e)
                )

            if not serializer.is_valid():
                lg.log_error(
                    message="[VALIDATE_SERIALIZER][INVALID]",
                    errors=serializer.errors
                )
                return ResponseBuilder.build(
                    ResponseCodes.INVALID_INPUT,
                    errors=serializer.errors
                )

            lg.log_info(
                message="[VALIDATE_SERIALIZER][SUCCESS]"
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
                    message="[EXCEPTION][UNHANDLED]"
                )
                return ResponseBuilder.build(
                    ResponseCodes.SYSTEM_ERROR,
                )
        return wrapper
    return decorator


def token_required():
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if 'Token' not in request.headers:
                lg.log_error(
                    message="[TOKEN][MISSING]",
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
                if error_format:
                    lg.log_error(
                        message="[TOKEN][INVALID]",
                        error_code=error_format
                    )
                    return ResponseBuilder.build(error_format)
                serializer = InfoTokenSerializer(data = data)
                if not serializer.is_valid():
                    lg.log_error(
                        message="[TOKEN][INVALID_DATA]",
                        errors=serializer.errors
                    )
                    return ResponseBuilder.build(
                        ResponseCodes.TOKEN_INVALID_TOKEN,
                        errors=serializer.errors
                    )
                
                lg.log_info(
                    message="[TOKEN][SUCCESS]",
                    data=serializer.validated_data
                )
                request.data_decode_token = serializer.validated_data
            except Exception as e:
                lg.log_error(
                    message="[TOKEN][DECODE_EXCEPTION]",
                )
                return ResponseBuilder.build(
                    ResponseCodes.SYSTEM_ERROR
                )
            return func(self, request, *args, **kwargs)

        return wrapper
    return decorator


def check_permission(permission_list: list):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            data_token = request.data_decode_token
            cache_permission = RedisService.get(data_token.get("jti"), alias="auth")
            if not cache_permission:
                lg.log_error(
                    message="[PERMISSION][CACHE_MISS]",
                    jti=data_token.get("jti")
                )
                return ResponseBuilder.build(
                    ResponseCodes.FORBIDDEN
                )
            if not all(permission in cache_permission.get('list_permission', []) for permission in permission_list):
                return ResponseBuilder.build(
                    ResponseCodes.FORBIDDEN
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

def rate_limit_ip(limit=5, window=60):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            ip = RequestLogger._get_client_ip(request)
            key = f"rate_limit:ip:{ip}"

            allowed = RedisService.rate_limit(key, limit, window)

            if not allowed:
                lg.log_error(
                    message="[RATE_LIMIT][EXCEEDED]",
                    ip=ip
                )
                return ResponseBuilder.build(
                    ResponseCodes.SYSTEM_BUSY,
                    errors="Quá nhiều yêu cầu từ địa chỉ IP này. Vui lòng thử lại sau."
                )

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

def track_execution(func_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            start = time.perf_counter()
            lg.log_info(
                message=f"[{func_name}][CALL]"
            )
            try:
                result = func(self, request, *args, **kwargs)
            finally:
                end = time.perf_counter()
                duration_ms = (end - start) * 1000
                lg.log_info(
                    message=f"[{func_name}][END CALL]",
                    duration_ms=duration_ms
                )
            return result
        return wrapper
    return decorator




