from rest_framework.views import APIView

from ...utils.tasks import send_mail_task

from ...shared.response import ResponseBuilder, ResponseCodes

from ..models.send_mail import TemplateEmail

from ..serializers.send_mail import SendMailInputSerializer
from ...shared.decorator.decorator import validate_exception, validate_serializer

class SendMailAPIView(APIView):
    @validate_exception()
    @validate_serializer(serializer_class=SendMailInputSerializer)
    def post(self, request, *args, **kwargs):
        data_input = request.validated_data
        template_email = TemplateEmail.objects.filter(id=data_input['template_id'], is_active=True).first()
        if not template_email:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors={"template": ["Template email không tồn tại hoặc đã bị vô hiệu hóa."]}
            )
        html = template_email.format
        body = data_input.get("body", {})
        for key, value in body.items():
            html = html.replace(f"{{{key}}}", str(value))
        send_mail_task.delay(
            subject=data_input['subject'],
            to=data_input['mail_to'],
            html_message=html
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
        )
        