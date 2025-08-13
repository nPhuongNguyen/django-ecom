from rest_framework.response import Response
from rest_framework import serializers
from functools import wraps

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
