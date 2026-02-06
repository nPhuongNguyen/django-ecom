from rest_framework.views import APIView

from ...auths.models.roles import RolePermissions

from ...config.redis_config import RedisService
from ecom.settings import TOKEN_SECRET_KEY

from ...utils.utils_token import encode_token

from ...shared.response import ResponseBuilder, ResponseCodes

from ...auths.models.users import UserRoles, Users

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
        
        #Lấy permissions và roles của user
        list_role = UserRoles.objects.filter(user_id=user_db.id, is_active=True).values_list('role_id', flat=True)
        permission_codes = (
            RolePermissions.objects
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
            UserRoles.objects
            .filter(
                user_id=user_db.id,
                is_active=True,
                role__is_active=True
            )
            .values_list('role__code', flat=True)
        )

        key_redis_user_login = str(uuid.uuid4())
        value_redis_user_login = {
            "id": str(user_db.id),
            "email": user_db.email,
            "is_super": str(user_db.is_super),
            "list_permission": list(permission_codes),
            "list_role_code": list(role_codes)
        }
        RedisService.set(
            key=key_redis_user_login,
            value=value_redis_user_login,
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