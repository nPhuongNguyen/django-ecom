from rest_framework.views import APIView
from apps.core.schema.optionvalues import OptionValueSerializer

from apps.core.services.optionvalues import OptionValueService
from apps.utils.decorator import *
from apps.utils.response import ResponseFormat as res
# Create your views here.

class OptionValueView(APIView):
    @catch_exceptions
    @validate_serializer(OptionValueSerializer)
    def post(self, request):
        serializer = request.validated_data
        option_value = OptionValueService.create_option_value(serializer)
        return res.response_success(data=option_value)
    @catch_exceptions
    def get(self, request, id=None):
        if id:
            option_value = OptionValueService.get_option_value_by_id(id)
            if not option_value:
                return res.response_error(message="Option Value không tồn tại!")
            return res.response_success(data=option_value)
        options_value = OptionValueService.get_all_options_value()
        return res.response_success(data=options_value)
    @catch_exceptions
    @validate_serializer(OptionValueSerializer)
    def put(self, request, id, *args, **kwargs):
        validated_data = request.validated_data
        option_value = OptionValueService.update_option_value(id, validated_data)
        if not option_value:
            return res.response_error(message="Option Value không tồn tại!")
        return res.response_success(message="Cập nhật Option Value thành công", data=option_value)
    @catch_exceptions
    def delete(self, request, id, *args, **kwargs):
        option_value = OptionValueService.delete_option_value(id)
        if not option_value:
            return res.response_error(message="Option Value không tồn tại!")
        return res.response_success(message="Xóa Option Value thành công", data=[])
