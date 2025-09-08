from rest_framework.views import APIView
from apps.core.schema.categories import *
from apps.core.services.categories import CategoryService
from apps.utils.decorator import *
from apps.utils.response import ResponseUtil as res
# Create your views here.

class CategoryView(APIView):
    @catch_exceptions
    @validate_serializer(CategoryInputSerializer)
    def post(self, request):
        serializer = request.validated_data
        category = CategoryService.create_category(serializer)

        return res.response_success(data=category)

    @catch_exceptions
    def get(self, request, sku=None):
        if sku:
            category = CategoryService.get_category_by_sku(sku)
            if not category:
                return res.response_error(message="Category không tồn tại!")
            return res.response_success(data=category)
        # Nếu không có slug → trả về list
        categories = CategoryService.get_all_categories()
        return res.response_success(data=categories)

    @catch_exceptions
    @validate_serializer(CategorySerializer)
    def put(self, request, sku, *args, **kwargs):
        validated_data = request.validated_data
        category = CategoryService.update_category(sku, validated_data)
        if not category:
            return res.response_error(message="Category không tồn tại!")
        return res.response_success(data=category)

    @catch_exceptions
    def delete(self, request, sku, *args, **kwargs):
        category = CategoryService.delete_category(sku)
        if not category:
            return res.response_error(message="Category không tồn tại!")
        return res.response_success(message="Xóa danh mục thành công", data=category)
