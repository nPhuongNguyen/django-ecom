
from rest_framework.views import APIView

from ...utils.tasks import send_mail_task


from ...auths.serializers.users import UserCreateSerializer

from ...auths.models.users import Users

from ...shared.response import ResponseBuilder, ResponseCodes

from ...shared.decorator.decorator import validate_exception, validate_serializer
from django.contrib.auth.hashers import make_password
from ..serializers.register import RegisterInputSerializer
class RegisterAPI(APIView):
    @validate_exception()
    @validate_serializer(serializer_class=RegisterInputSerializer)
    def post(self, request, *args, **kwargs):
        data_input = request.validated_data
        email = data_input.get('email')
        password = data_input.get('password')
        confirm_password = data_input.get('confirm_password')
        hashed_password = make_password(password)
        serializer = UserCreateSerializer(data = {
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
            "is_super": False,
            "is_active": False
        })
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        serializer.save(password=hashed_password)
        send_mail_task.delay(
            subject="Register success",
            to=[email],
            html_message="<h1>Hello</h1>"
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS
        )