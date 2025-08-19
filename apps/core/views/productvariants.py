from rest_framework.views import APIView
from apps.core.schema.products import *
from apps.core.schema.productvariants import *
from apps.core.services.products import ProductService

from apps.core.services.productvariants import ProductVariantService
from apps.utils.decorator import *
from rest_framework.response import Response
# Create your views here.

class ProductVariantView(APIView):
    @catch_exceptions
    @validate_serializer(ProductVariantInputSerializer)
    def post(self, request):
        serializer = request.validated_data
        product_variant = ProductVariantService.create_product_variant(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": product_variant
            }
        )
    @catch_exceptions
    def get(self, request, sku=None):
        if sku:
            product_variant = ProductVariantService.get_product_variant_by_sku(sku)
            if not product_variant:
                return Response({
                    "statusCode": 0,
                    "message": "Sản phẩm Variant không tồn tại!",
                    "data": None
                })
            return Response({
                "statusCode": 1,
                "message": "Thành công",
                "data": product_variant
            })
        products_variant = ProductVariantService.get_all_products_variant()
        return Response({
            "statusCode": 1,
            "message": "Thành công",
            "data": products_variant
        })

    @catch_exceptions
    @validate_serializer(ProductVariantSerializer)
    def put(self, request, sku, *args, **kwargs):
        validated_data = request.validated_data 
        product_variant = ProductVariantService.update_product_variant(sku, validated_data)
        if not product_variant:
            return Response({
                "statusCode": 0,
                "message": "Sản phẩm Variant không tồn tại!",
                "data": None
            })
        return Response({
            "statusCode": 1,
            "message": "Cập nhật sản phẩm Variant thành công",
            "data": product_variant
        })
    @catch_exceptions
    def delete(self, request, slug, *args, **kwargs):
        product = ProductService.delete_product(slug)
        if not product:
            return Response({
                "statusCode": 0,
                "message": "Sản phẩm không tồn tại!",
                "data": None
            })
        
        return Response({
            "statusCode": 1,
            "message": "Xóa sản phẩm thành công",
            "data": product
        })
    
