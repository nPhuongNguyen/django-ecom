
from rest_framework.views import APIView

from ...utils.generate_otp import generate_otp


from ...config.redis_config import RedisService

from ...utils.tasks import send_mail_task


from ...auths.serializers.users import UserCreateSerializer

from ...auths.models.users import Users

from ...shared.response import ResponseBuilder, ResponseCodes
from apps.logging import logging_log as lg
from ...shared.decorator.decorator import validate_exception, validate_serializer
from django.contrib.auth.hashers import make_password
from ..serializers.register import RegisterConfirmInputSerializer, RegisterInputSerializer
class RegisterAPI(APIView):
    @validate_exception()
    @validate_serializer(serializer_class=RegisterInputSerializer)
    def post(self, request, *args, **kwargs):
        #Data input
        data_input = request.validated_data
        email = data_input.get('email')
        password = data_input.get('password')
        confirm_password = data_input.get('confirm_password')
        #hash password
        hashed_password = make_password(password)
        serializer = UserCreateSerializer(data = {
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
            "is_super": False,
            "is_active": False
        })
        #Check validate serializer
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        #Saver user
        serializer.save(password=hashed_password)
        #Cache OTP
        instance = serializer.instance
        otp = generate_otp()
        RedisService.set(
            key=f"register:{otp}:{instance.id}",
            value={
                "otp": otp
            },
            timeout=300, #5 minutes
            alias="auth"
        )
        #Send mail
        send_mail_task.delay(
            subject="Register success",
            to=[email],
            html_message=f"<h1>Hello, your OTP is: {otp}</h1>"
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS
        )
    

class RegisterConfirmAPI(APIView):
    @validate_exception()
    @validate_serializer(serializer_class=RegisterConfirmInputSerializer)
    def post(self, request, *args, **kwargs):
        data_input = request.validated_data
        email = data_input.get('email')
        confirmation_code = data_input.get('confirmation_code')
        check_user = Users.objects.filter(email=email).first()
        #Check OTP in Redis
        cached_data = RedisService.get(key=f"register:{confirmation_code}:{check_user.id}", alias="auth")
        if not cached_data:
            return ResponseBuilder.build(
                code=ResponseCodes.OTP_INVALID
            )
        #Update user is_active = True
        Users.objects.filter(email=email).update(is_active=True)
        #Delete cache OTP
        RedisService.delete(key=f"register:{confirmation_code}:{email}", alias="auth")
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS
        )