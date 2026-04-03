from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from apps.logging import logging_log as lg
from apps.catalogue.serializers.upload import UploadImageSerializer
from ...shared.decorator.decorator import validate_exception
from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.utils.utils_handle_upload import handle_upload

class UploadImageAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]
    # @token_required()
    @validate_exception()
    def post(self, request, *args, **kwargs):
        data_input = request.files
        serializer = UploadImageSerializer(data=data_input)
        if not serializer.is_valid():
            lg.log_error(
                "[UploadImageAPI] Invalid input",
                errors=serializer.errors
            )
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        validated_data = serializer.validated_data
        input_img = validated_data.get('list_image')
        folder = "product"
        result_img = handle_upload(input_img, folder)
        if result_img is None:
            lg.log_error(
                "[UploadImageAPI] Upload failed",
                folder=folder
            )
            return ResponseBuilder.build(
               code=ResponseCodes.SYSTEM_BUSY,
               errors="Lỗi upload"
            )
        lg.log_info(
            "[UploadImageAPI] Upload successful",
            folder=folder,
            result=result_img
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data = {
                'list_img': result_img
            }
        )