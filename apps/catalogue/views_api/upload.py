from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from apps.catalogue.serializers.upload import UploadImageSerializer
from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.utils.utils_handle_upload import handle_upload

class UploadImageAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]
    # @token_required()
    def post(self, request, *args, **kwargs):
        data_input = request.data_input
        serializer = UploadImageSerializer(data=data_input)
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        validated_data = serializer.validated_data
        data_body_input = validated_data.get("body", {})
        input_img = data_body_input.get('list_image')
        folder = "product"
        result_img = handle_upload(input_img, folder)
        if result_img is None:
            return ResponseBuilder.build(
               code=ResponseCodes.SYSTEM_BUSY,
               errors="Lỗi upload"
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data = {
                'list_img': result_img
            }
        )