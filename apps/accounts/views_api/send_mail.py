from rest_framework.views import APIView

from ...utils.tasks import send_mail_task

from ...shared.response import ResponseBuilder, ResponseCodes

from ..models.send_mail import TemplateEmail

from ..serializers.send_mail import SendMailInputSerializer
from ...shared.decorator.decorator import validate_exception

class SendMailAPIView(APIView):
    @validate_exception()
    def post(self, request, *args, **kwargs):
        data_input = request.data_input
        data_input_body = data_input.get("body", {})
        serializer = SendMailInputSerializer(data=data_input_body)
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        data_input_safe = serializer.validated_data
        data_input_body = data_input_safe.get("body", {})
        template_email = TemplateEmail.objects.filter(id=data_input_body.get("template_id"), is_active=True).first()
        if not template_email:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={"template": ["Template email không tồn tại hoặc đã bị vô hiệu hóa."]}
            )
        html = template_email.format
        body = data_input_body.get("body", {})
        for key, value in body.items():
            html = html.replace(f"{{{key}}}", str(value))
        send_mail_task.delay(
            subject=data_input_safe.get("subject"),
            to=data_input_safe.get("mail_to"),
            html_message=html
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
        )
        