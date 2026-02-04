from rest_framework.views import APIView

from ...config.redis_config import RedisService
from ecom.settings import TOKEN_SECRET_KEY

from ...utils.utils_token import encode_token

from ...shared.response import ResponseBuilder, ResponseCodes

from ...auths.models.users import Users

from ..serializers.login import LoginInputSerializer

from ...shared.decorator.decorator import validate_exception, validate_serializer
from django.contrib.auth.hashers import check_password
import uuid

class LoginAPI(APIView):
    @validate_exception()
    @validate_serializer(serializer_class=LoginInputSerializer)
    def post(self, request, *args, **kwargs):
        data_input = request.validated_data
        email_input = data_input.get('user_email')
        password_input = data_input.get('user_password')
        remember_me_input = data_input.get('remember_me')
        user_db = Users.objects.filter(email=email_input).first()
        if not user_db:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={
                    "email": "Email không tồn tại."
                }
            )
        if not check_password(password_input, user_db.password):
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={
                    "password": "Mật khẩu không đúng."
                }
            )
        if not user_db.is_active:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={
                    "email": "Email chưa được kích hoạt."
                }
            )
        key_redis_user_login = str(uuid.uuid4())
        RedisService.set(
            key=key_redis_user_login,
            value={
                "id": str(user_db.id),
                "email": user_db.email,
                "is_super": str(user_db.is_super),
            },
            alias="auth"
        )
        _encode_token = encode_token(key_redis_user_login, TOKEN_SECRET_KEY)
        if not _encode_token:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=_encode_token
        )