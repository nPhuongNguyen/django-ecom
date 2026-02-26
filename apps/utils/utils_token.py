
from datetime import timedelta
from django.utils import timezone
import uuid
import jwt
from apps.shared.response import ResponseCodes
from apps.logging import logging_log as lg
def encode_token(jti: str, secret_key: str)-> str:
    encode_token = None
    try:
        now = timezone.now()
        payload = {
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(hours=2)).timestamp()),
            "jti": jti
        }
        encode_token = jwt.encode(payload, secret_key, algorithm="HS256")
    except Exception:
        lg.log_error(
            message="Encode token thất bại!"
        )
    return encode_token


def decode_token(token: str, secret_key: str = None):
    try:
        payload = jwt.decode(token, secret_key,  algorithms="HS256")
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, ResponseCodes.TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return None, ResponseCodes.TOKEN_INVALID_TOKEN
    
def normalize_token(token: str)->str|None:
    if not token:
        lg.log_error(
            message="Token không được cung cấp!"
        )
        return None
    parts = token.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
        lg.log_info(
            message="Token đã được chuẩn hóa!",
            token=token
        )
    return token



