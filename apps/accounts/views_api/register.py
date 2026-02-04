
from rest_framework.views import APIView

from ..models.send_mail import TemplateEmail

from ...utils.generate_otp import generate_otp


from ...config.redis_config import RedisService

from ...utils.tasks import send_mail_task


from ...auths.serializers.users import UserCreateSerializer

from ...auths.models.users import Users

from ...shared.response import ResponseBuilder, ResponseCodes
from apps.logging import logging_log as lg
from ...shared.decorator.decorator import validate_exception, validate_serializer
from ..serializers.register import RegisterConfirmInputSerializer, RegisterInputSerializer
from django.db import transaction
class RegisterAPI(APIView):
    @validate_exception()
    @validate_serializer(serializer_class=RegisterInputSerializer)
    def post(self, request, *args, **kwargs):
        #Data input
        data_input = request.validated_data
        email = data_input.get('email')
        serializer = UserCreateSerializer(data = data_input)
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
            RedisService.set(
                key=f"register:otp:{instance.id}",
                value={
                    "otp": otp
                },
                timeout=300, #5 minutes
                alias="auth"
            )
            html = template_email.format
            html = html.replace("{otp}", otp)
            #Send mail
            send_mail_task.delay(
                subject="OTP Register",
                to=[email],
                html_message=html
            )
            return ResponseBuilder.build(
                code=ResponseCodes.SUCCESS
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SYSTEM_ERROR
        )
    
class RegisterConfirmAPI(APIView):
    @validate_exception()
    @validate_serializer(serializer_class=RegisterConfirmInputSerializer)
    def post(self, request, *args, **kwargs):
        data_input = request.validated_data
        email = data_input.get('email')
        confirmation_code = data_input.get('confirmation_code')
        check_user = Users.objects.filter(email=email, is_active=False).first()
        if not check_user:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={"email": ["Người dùng không tồn tại hoặc đã được kích hoạt."]}
            )
        #Check OTP in Redis
        cached_data = RedisService.get(key=f"register:otp:{check_user.id}", alias="auth")
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
        RedisService.delete(key=f"register:otp:{check_user.id}", alias="auth")
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS
        )