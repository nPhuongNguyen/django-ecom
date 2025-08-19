from rest_framework.views import APIView
from apps.core.schema.options import OptionSerializer
from apps.core.services.options import OptionService

from apps.utils.decorator import *
from rest_framework.response import Response
# Create your views here.

class OptionView(APIView):
    @catch_exceptions
    @validate_serializer(OptionSerializer)
    def post(self, request):
        serializer = request.validated_data
        option = OptionService.create_option(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": option
            }
        )
    @catch_exceptions
    def get(self, request, id=None):
        if id:
            option = OptionService.get_option_by_id(id)
            if not option:
                return Response({
                    "statusCode": 0,
                    "message": "Option không tồn tại!",
                    "data": None
                })
            return Response({
                "statusCode": 1,
                "message": "Thành công",
                "data": option
            })
        options = OptionService.get_all_options()
        return Response({
            "statusCode": 1,
            "message": "Thành công",
            "data": options
        })

    @catch_exceptions
    @validate_serializer(OptionSerializer)
    def put(self, request, id, *args, **kwargs):
        validated_data = request.validated_data 
        option = OptionService.update_option(id, validated_data)
        if not option:
            return Response({
                "statusCode": 0,
                "message": "Option không tồn tại!",
                "data": None
            })
        return Response({
            "statusCode": 1,
            "message": "Cập nhật Option thành công",
            "data": option
        })
    @catch_exceptions
    def delete(self, request, id, *args, **kwargs):
        option = OptionService.delete_option(id)
        if not option:
            return Response({
                "statusCode": 0,
                "message": "Option không tồn tại!",
                "data": None
            })
        
        return Response({
            "statusCode": 1,
            "message": "Xóa Option thành công",
            "data": option
        })
    
