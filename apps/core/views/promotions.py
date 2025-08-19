from rest_framework.views import APIView
from apps.core.schema.products import ProductOutputSerializer, ProductSerializer
from apps.core.schema.promotions import PromotionOutputSerializer, PromotionSerializer
from apps.core.services.products import ProductService
from apps.core.services.promotions import PromotionService
from apps.utils.decorator import *
from rest_framework.response import Response
# Create your views here.

class PromotionView(APIView):
    @catch_exceptions
    @validate_serializer(PromotionSerializer)
    def post(self, request):
        serializer = request.validated_data
        promotion = PromotionService.create_promotion(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": promotion
            }
        )
    @catch_exceptions
    def get(self, request, slug=None):
        if slug:
            promotion = PromotionService.get_promotion_by_slug(slug)
            if not promotion:
                return Response({
                    "statusCode": 0,
                    "message": "Promotion không tồn tại!",
                    "data": None
                })
            return Response({
                "statusCode": 1,
                "message": "Thành công",
                "data": promotion
            })
        # Nếu không có slug → trả về list
        promotions = PromotionService.get_all_promotions()
        return Response({
            "statusCode": 1,
            "message": "Thành công",
            "data": promotions
        })

    @catch_exceptions
    @validate_serializer(PromotionSerializer)
    def put(self, request, slug, *args, **kwargs):
        validated_data = request.validated_data 
        promotion = PromotionService.update_promotion(slug, validated_data)
        if not promotion:
            return Response({
                "statusCode": 0,
                "message": "Promotion không tồn tại!",
                "data": None
            })
        return Response({
            "statusCode": 1,
            "message": "Cập nhật Promotion thành công",
            "data": promotion
        })
    @catch_exceptions
    def delete(self, request, slug, *args, **kwargs):
        promotion = PromotionService.delete_promotion(slug)
        if not promotion:
            return Response({
                "statusCode": 0,
                "message": "Promotion không tồn tại!",
                "data": None
            })
        
        return Response({
            "statusCode": 1,
            "message": "Xóa sản phẩm thành công",
            "data": promotion
        })
    
