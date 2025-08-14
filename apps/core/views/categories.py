from rest_framework.views import APIView
from apps.core.schema.categories import CategorySerializer
from apps.core.services.categories import CategoryService
from apps.utils.decorator import validate_serializer
from rest_framework.response import Response
# Create your views here.

class CategoryView(APIView):
    @validate_serializer(CategorySerializer)
    def post(self, request):
        serializer = request.validated_data
        category = CategoryService.create_category(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": CategorySerializer(category).data
            }
        )
    def get(self, request, sku=None):
        if sku:
            category = CategoryService.get_category_by_sku(sku)
            if not category:
                return Response({
                    "statusCode": 0,
                    "message": "Category not found",
                    "data": None
                })
            return Response({
                "statusCode": 1,
                "message": "Thành công",
                "data": CategorySerializer(category).data
            })
        # Nếu không có slug → trả về list
        categories = CategoryService.get_all_categories()
        return Response({
            "statusCode": 1,
            "message": "Thành công",
            "data": CategorySerializer(categories, many=True).data
        })


    @validate_serializer(CategorySerializer)
    def put(self, request, sku, *args, **kwargs):
        validated_data = request.validated_data
        category = CategoryService.update_category(sku, validated_data)
        if not category:
            return Response({
                "statusCode": 0,
                "message": "Category not found",
                "data": None
            })
        return Response({
            "statusCode": 1,
            "message": "Cập nhật danh mục thành công",
            "data": CategorySerializer(category).data
        })
    
    def delete(self, request, sku, *args, **kwargs):
        category = CategoryService.delete_category(sku)
        if not category:
            return Response({
                "statusCode": 0,
                "message": "Category not found",
                "data": None
            })
        
        return Response({
            "statusCode": 1,
            "message": "Xóa danh mục thành công",
            "data": CategorySerializer(category).data
        })
    
