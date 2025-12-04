__all__ = [
    'ResponseCode',
    'ResponseCodes',
    'ResponseBuilder',
]

from typing import Any
from rest_framework.response import Response


class ResponseCode:
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class ResponseCodes:
    SUCCESS = ResponseCode(1, "Thành công.")
    SYSTEM_ERROR = ResponseCode(500, "Lỗi hệ thống, vui lòng thử lại sau.")
    SYSTEM_BUSY = ResponseCode(800, "Hệ thống đang bận, vui lòng thử lại sau.")
    INVALID_INPUT = ResponseCode(400, "Dữ liệu không hợp lệ.")
    

class ResponseBuilder:
    @staticmethod
    def build(code: ResponseCode, data: Any = None, errors: Any = None):
        response_body = {
            'status_code': code.status_code,
            'message': code.message,
            'data': data,
            'errors': errors
        }
        return Response(response_body, status=200)
