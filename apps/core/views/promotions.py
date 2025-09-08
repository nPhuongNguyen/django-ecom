from rest_framework.views import APIView
from apps.core.schema.promotions import PromotionSerializer
from apps.core.services.promotions import PromotionService
from apps.utils.decorator import *
from apps.utils.response import ResponseUtil as res
# Create your views here.

class PromotionView(APIView):
    @catch_exceptions
    @validate_serializer(PromotionSerializer)
    def post(self, request):
        serializer = request.validated_data
        promotion = PromotionService.create_promotion(serializer)
        return res.response_success(data=promotion)
    @catch_exceptions
    def get(self, request, slug=None):
        if slug:
            promotion = PromotionService.get_promotion_by_slug(slug)
            if not promotion:
                return res.response_error(message="Promotion không tồn tại!")
            return res.response_success(data=promotion)
        # Nếu không có slug → trả về list
        promotions = PromotionService.get_all_promotions()
        return res.response_success(data=promotions)

    @catch_exceptions
    @validate_serializer(PromotionSerializer)
    def put(self, request, slug, *args, **kwargs):
        validated_data = request.validated_data
        promotion = PromotionService.update_promotion(slug, validated_data)
        if not promotion:
            return res.response_error(message="Promotion không tồn tại!")
        return res.response_success(message="Cập nhật Promotion thành công", data=promotion)
    @catch_exceptions
    def delete(self, request, slug, *args, **kwargs):
        promotion = PromotionService.delete_promotion(slug)
        if not promotion:
            return res.response_error(message="Promotion không tồn tại!")
        return res.response_success(message="Xóa sản phẩm thành công", data=promotion)
