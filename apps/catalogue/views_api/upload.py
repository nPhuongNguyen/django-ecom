from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from apps.catalogue.serializers.upload import UploadImageSerializer
from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.utils.decorator import validate_serializer
from apps.utils.utils_handle_upload import handle_upload

class UploadImageAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]
    # @token_required()
    @validate_serializer(serializer_class=UploadImageSerializer)
    def post(self, request, *args, **kwargs):
        validated_data = request.validated_data
        iput_img = validated_data.get('list_image')
        folder = "product"
        result_img = handle_upload(iput_img, folder)
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