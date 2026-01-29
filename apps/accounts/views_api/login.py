from rest_framework.views import APIView

from ecom.settings import TOKEN_SECRET_KEY

from ...utils.utils_token import encode_token

from ...shared.response import ResponseBuilder, ResponseCodes

from ...auths.models.users import Users

from ..serializers.login import LoginInputSerializer

from ...shared.decorator.decorator import validate_exception, validate_serializer
from django.contrib.auth.hashers import check_password, make_password

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
                code=ResponseCodes.LOGIN_FAILD_INPUT
            )
        if not check_password(password_input, user_db.password):
            return ResponseBuilder.build(
                code=ResponseCodes.LOGIN_FAILD_INPUT
            )
        if not user_db.is_active:
            return ResponseBuilder.build(
                code=ResponseCodes.LOGIN_FAILD_IS_ACTIVE
            )
        data_output = {
            "email":user_db.email,
            "permission":[],
            "is_super":user_db.is_super
        }
        _encode_token = encode_token(data_output, TOKEN_SECRET_KEY)
        if not _encode_token:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=_encode_token
        )