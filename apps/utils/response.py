"""Tiện ích tạo response chuẩn cho API."""

from rest_framework.response import Response

class ResponseFormat:
    @staticmethod
    def response_success(message="Thành công", data=None):
        return Response({
            "statusCode": 1,
            "message": message,
            "data": data
        })

    @staticmethod
    def response_error(message="Có lỗi xảy ra", data=None):
        return Response({
            "statusCode": 0,
            "message": message,
            "data": data
    })
