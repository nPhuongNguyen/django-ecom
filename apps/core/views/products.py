from rest_framework.views import APIView
from apps.core.schema.products import ProductSerializer
from apps.core.services.products import ProductService

from apps.utils.decorator import *
from apps.utils.response import ResponseFormat as res
# Create your views here.

class ProductView(APIView):
    @catch_exceptions
    @validate_serializer(ProductSerializer)
    def post(self, request):
        serializer = request.validated_data
        product = ProductService.create_product(serializer)
        return res.response_success(data=product)

    @catch_exceptions
    def get(self, request, slug=None):
        if slug:
            product = ProductService.get_product_by_slug(slug)
            if not product:
                return res.response_error(message="Sản phẩm không tồn tại!")
            return res.response_success(data=product)
        products = ProductService.get_all_products()
        return res.response_success(data=products)

    @catch_exceptions
    @validate_serializer(ProductSerializer)
    def put(self, request, slug, *args, **kwargs):
        validated_data = request.validated_data
        product = ProductService.update_product(slug, validated_data)
        if not product:
            return res.response_error(message="Sản phẩm không tồn tại!")
        return res.response_success(message="Cập nhật sản phẩm thành công", data=product)
    @catch_exceptions
    def delete(self, request, slug, *args, **kwargs):
        product = ProductService.delete_product(slug)
        if not product:
            return res.response_error(message="Sản phẩm không tồn tại!")
        return res.response_success(message="Xóa sản phẩm thành công", data=product)
