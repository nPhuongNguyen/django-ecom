from rest_framework.views import APIView
from apps.core.schema import ProductSerializer
from apps.core.services.products import ProductService
from apps.utils.decorator import validate_serializer
from rest_framework.response import Response
# Create your views here.

class ProductView(APIView):
    @validate_serializer(ProductSerializer)
    def post(self, request):
        serializer = request.validated_data
        product = ProductService.create_product(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": ProductSerializer(product).data
            }
        )
    def get(self, request):
        products = ProductService.get_all_products()
        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": ProductSerializer(products, many=True).data
            }
        )
    
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
            "data": ProductSerializer(product).data
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
            "data": ProductSerializer(product).data
        })