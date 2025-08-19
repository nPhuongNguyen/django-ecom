from rest_framework.views import APIView
from apps.core.schema.products import ProductOutputSerializer, ProductSerializer
from apps.core.services.products import ProductService

from apps.utils.decorator import *
from rest_framework.response import Response
# Create your views here.

class ProductView(APIView):
    @catch_exceptions
    @validate_serializer(ProductSerializer)
    def post(self, request):
        serializer = request.validated_data
        product = ProductService.create_product(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": product
            }
        )
    @catch_exceptions
    def get(self, request, slug=None):
        if slug:
            product = ProductService.get_product_by_slug(slug)
            if not product:
                return Response({
                    "statusCode": 0,
                    "message": "Sản phẩm không tồn tại!",
                    "data": None
                })
            return Response({
                "statusCode": 1,
                "message": "Thành công",
                "data": product
            })
        products = ProductService.get_all_products()
        return Response({
            "statusCode": 1,
            "message": "Thành công",
            "data": products
        })

    @catch_exceptions
    @validate_serializer(ProductSerializer)
    def put(self, request, slug, *args, **kwargs):
        validated_data = request.validated_data 
        product = ProductService.update_product(slug, validated_data)
        if not product:
            return Response({
                "statusCode": 0,
                "message": "Sản phẩm không tồn tại!",
                "data": None
            })
        return Response({
            "statusCode": 1,
            "message": "Cập nhật sản phẩm thành công",
            "data": product
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
    
