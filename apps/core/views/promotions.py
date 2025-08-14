from rest_framework.views import APIView
from apps.core.schema.products import ProductOutputSerializer, ProductSerializer
from apps.core.schema.promotions import PromotionOutputSerializer, PromotionSerializer
from apps.core.services.products import ProductService
from apps.core.services.promotions import PromotionService
from apps.utils.decorator import validate_serializer
from rest_framework.response import Response
# Create your views here.

class PromotionView(APIView):
    @validate_serializer(PromotionSerializer)
    def post(self, request):
        serializer = request.validated_data
        promotion = PromotionService.create_promotion(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": PromotionOutputSerializer(promotion).data
            }
        )
    def get(self, request, slug=None):
        if slug:
            product = ProductService.get_product_by_slug(slug)
            if not product:
                return Response({
                    "statusCode": 0,
                    "message": "Product not found",
                    "data": None
                })
            return Response({
                "statusCode": 1,
                "message": "Thành công",
                "data": ProductOutputSerializer(product).data
            })
        # Nếu không có slug → trả về list
        promotions = PromotionService.get_all_promotions()
        return Response({
            "statusCode": 1,
            "message": "Thành công",
            "data": PromotionOutputSerializer(promotions, many=True).data
        })

    
    @validate_serializer(ProductSerializer)
    def put(self, request, slug, *args, **kwargs):
        validated_data = request.validated_data 
        product = ProductService.update_product(slug, validated_data)
        if not product:
            return Response({
                "statusCode": 0,
                "message": "Product not found",
                "data": None
            })
        return Response({
            "statusCode": 1,
            "message": "Cập nhật sản phẩm thành công",
            "data": ProductOutputSerializer(product).data
        })
    
    def delete(self, request, slug, *args, **kwargs):
        product = ProductService.delete_product(slug)
        if not product:
            return Response({
                "statusCode": 0,
                "message": "Product not found",
                "data": None
            })
        
        return Response({
            "statusCode": 1,
            "message": "Xóa sản phẩm thành công",
            "data": ProductOutputSerializer(product).data
        })
    
