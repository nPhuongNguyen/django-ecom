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

    TOKEN_REQUIRED = ResponseCode(1000, "Token không tồn tại")
    TOKEN_EXPIRED = ResponseCode(1001, "Token hết hạn")
    TOKEN_INVALID_TOKEN = ResponseCode(1002, "Token không hợp lệ")
    TOKEN_APP_ERROR = ResponseCode(10403, "unauthorized")

    #Phiên đăng nhập
    LOGIN_FAILD_INPUT = ResponseCode(400, "Tài khoản hoặc mật khẩu không đúng.")
    LOGIN_FAILD_IS_ACTIVE = ResponseCode(400, "Tài khoản của bạn đã bị khóa.")

    #Phiên đăng kí
    REGISTER_EMAIL_EXISTS = ResponseCode(400, "Email đã tồn tại.")
    REGISTER_PASSWORD_MISMATCH = ResponseCode(400, "Mật khẩu không khớp.")

    #Xác thực OTP
    OTP_INVALID = ResponseCode(400, "Mã OTP không hợp lệ.")
    SUCCESS_VERIFY_OTP = ResponseCode(1, "Xác thực OTP thành công.")
    SUCCESS_RESEND_OTP = ResponseCode(1, "Gửi lại mã OTP thành công.")
    SUCCESS_OTP_EXPIRED = ResponseCode(400, "Mã OTP đã hết hạn, vui lòng yêu cầu mã mới.")
    SUCCESS_OTP_EXITS = ResponseCode(400, "Mã OTP đã được gửi, vui lòng kiểm tra email.")
    
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
