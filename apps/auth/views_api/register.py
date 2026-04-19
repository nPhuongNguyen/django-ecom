
from rest_framework.views import APIView

from ...accounts.models.users import Users

from ..models.send_mail import TemplateEmail

from ...utils.generate_otp import generate_otp


from ...config.redis_config import RedisService

from ...utils.tasks import send_mail_task


from ...accounts.serializers.users import UserCreateSerializer


from ...shared.response import ResponseBuilder, ResponseCodes
from apps.logging import logging_log as lg
from ...shared.decorator.decorator import validate_exception
from ..serializers.register import RegisterConfirmInputSerializer, RegisterResendOTPInputSerializer
from django.db import transaction
class RegisterAPI(APIView):
    redis_auth = RedisService('auth')
    @validate_exception()
    def post(self, request, *args, **kwargs):
        #Data input
        data_input = request.data_input
        data_input_body = data_input.get("body", {})
        email = data_input_body.get('email')
        serializer = UserCreateSerializer(data = data_input_body)
        #Check validate serializer
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        template_email = TemplateEmail.objects.filter(code="confirm-register", is_active=True).first()
        if not template_email:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
            )
        with transaction.atomic():
            #Saver user
            serializer.save()
            #Cache OTP
            instance = serializer.instance
            otp = generate_otp()
            self.redis_auth.set(
                key=f"register:otp:{instance.id}",
                value={
                    "otp": otp
                },
                timeout=300 #5 minutes
            )
            html = template_email.format
            html = html.replace("{otp}", otp)
            #Send mail
            # send_mail_task.delay(
            #     subject="OTP Register",
            #     to=[email],
            #     html_message=html
            # )
            return ResponseBuilder.build(
                code=ResponseCodes.SUCCESS
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SYSTEM_ERROR
        )
    
class RegisterConfirmAPI(APIView):
    redis_auth = RedisService('auth')
    @validate_exception()
    def post(self, request, *args, **kwargs):
        data_input = request.data_input
        data_input_body = data_input.get("body", {})
        serializer = RegisterConfirmInputSerializer(data=data_input_body)
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        data_input_safe = serializer.validated_data
        email = data_input_safe.get('email')
        confirmation_code = data_input_safe.get('confirmation_code')
        check_user = Users.objects.filter(email=email, is_active=False).first()
        if not check_user:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={"email": ["Người dùng không tồn tại hoặc đã được kích hoạt."]}
            )
        #Check OTP in Redis
        cached_data = self.redis_auth.get(key=f"register:otp:{check_user.id}")
        if not cached_data or cached_data.get("otp") != confirmation_code:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={
                    "confirmation_code": "Mã OTP không hợp lệ."
                }
            )
        #Update user is_active = True
        Users.objects.filter(id=check_user.id).update(is_active=True)
        #Delete cache OTP
        self.redis_auth.delete(key=f"register:otp:{check_user.id}")
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS
        )
    
class RegisterResendOTPAPI(APIView):
    redis_auth = RedisService('auth')
    @validate_exception()
    def post(self, request, *args, **kwargs):
        data_input = request.data_input
        data_input_body = data_input.get("body", {})
        serializer = RegisterResendOTPInputSerializer(data=data_input_body)
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        data_input_safe = serializer.validated_data
        email = data_input_safe.get('email')
        check_user = Users.objects.filter(email=email, is_active=False).first()
        if not check_user:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={"email": ["Người dùng không tồn tại hoặc đã được kích hoạt."]}
            )
        #Cache OTP
        check_otp_redis = self.redis_auth.get(key=f"register:otp:{check_user.id}")
        if check_otp_redis:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={"email": ["Mã OTP đã được gửi, vui lòng kiểm tra email."]}
            )
        else:
            otp = generate_otp()
            self.redis_auth.set(
                key=f"register:otp:{check_user.id}",
                value={
                    "otp": otp
                },
                timeout=300 #5 minutes
            )
            template_email = TemplateEmail.objects.filter(code="confirm-register", is_active=True).first()
            if not template_email:
                return ResponseBuilder.build(
                    code=ResponseCodes.INVALID_INPUT,
                )
            html = template_email.format
            html = html.replace("{otp}", otp)
            #Send mail
            # send_mail_task.delay(
            #     subject="OTP Register",
            #     to=[email],
            #     html_message=html
            # )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS
        )