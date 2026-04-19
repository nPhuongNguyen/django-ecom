from rest_framework.views import APIView

from ...accounts.models.user import User


from ..models.user_role import UserRole

from ..models.role_permission import RolePermission

from ..serializers.login import LoginInputSerializer


from ...config.redis_config import RedisService
from ecom.settings import TOKEN_SECRET_KEY

from ...utils.utils_token import encode_token

from ...shared.response import ResponseBuilder, ResponseCodes


from ...shared.decorator.decorator import validate_exception
from django.contrib.auth.hashers import check_password
import uuid

class LoginAPI(APIView):
    redis = RedisService(alias="auth")
    @validate_exception()
    def post(self, request, *args, **kwargs):
        data_input = request.data_input
        data_body_input = data_input.get("body", {})
        serializer = LoginInputSerializer(data=data_body_input)
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        data_body_safe = serializer.validated_data
        email_input = data_body_safe.get('user_email')
        password_input = data_body_safe.get('user_password')
        remember_me_input = data_body_safe.get('remember_me')
        user_db = User.objects.filter(email=email_input).first()
        if not user_db:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={
                    "email": "Email không tồn tại."
                }
            )
        if not user_db.is_active:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={
                    "email": "Email chưa được kích hoạt."
                }
            )
        if not check_password(password_input, user_db.password):
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={
                    "password": "Mật khẩu không đúng."
                }
            )
        #Lấy permissions và roles của user
        list_role = UserRole.objects.filter(user_id=user_db.id, is_active=True).values_list('role_id', flat=True)
        permission_codes = (
            RolePermission.objects
            .filter(
                role_id__in=list_role,
                is_active=True,
                permission__is_active=True,
                role__is_active=True,
            )
            .values_list('permission__code', flat=True)
            .distinct() # User có thể có nhiều role, nên cần distinct để tránh trùng lặp permission
        )
        role_codes = (
            UserRole.objects
            .filter(
                user_id=user_db.id,
                is_active=True,
                role__is_active=True
            )
            .values_list('role__code', flat=True)
        )

        jti = str(uuid.uuid4())
        key_redis_user_login = f"login:{jti}"
        value_redis_user_login = {
            "email": user_db.email,
            "is_super": str(user_db.is_super),
            "list_permission": list(permission_codes),
            "list_role_code": list(role_codes)
        }
        set_redis_user = self.redis.set(
            key=key_redis_user_login,
            value=value_redis_user_login,
        )

        if not set_redis_user:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR
            )
        
        _encode_token = encode_token(jti, TOKEN_SECRET_KEY)
        if not _encode_token:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=_encode_token
        )