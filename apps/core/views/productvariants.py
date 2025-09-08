from rest_framework.views import APIView
from apps.core.schema.products import *
from apps.core.schema.productvariants import *

from apps.core.services.productvariants import ProductVariantService
from apps.utils.decorator import *
from apps.utils.response import ResponseFormat as res
# Create your views here.

class ProductVariantView(APIView):
    @catch_exceptions
    @validate_serializer(ProductVariantInputSerializer)
    def post(self, request):
        serializer = request.validated_data
        product_variant = ProductVariantService.create_product_variant(serializer)
        return res.response_success(data=product_variant)
    @catch_exceptions
    def get(self, request, sku=None):
        if sku:
            product_variant = ProductVariantService.get_product_variant_by_sku(sku)
            if not product_variant:
                return res.response_error(message="Sản phẩm Variant không tồn tại!")
            return res.response_success(data=product_variant)
        products_variant = ProductVariantService.get_all_products_variant()
        return res.response_success(data=products_variant)
    @catch_exceptions
    @validate_serializer(ProductVariantSerializer)
    def put(self, request, sku, *args, **kwargs):
        validated_data = request.validated_data
        product_variant = ProductVariantService.update_product_variant(sku, validated_data)
        if not product_variant:
            return res.response_error(message="Sản phẩm Variant không tồn tại!")
        return res.response_success(message="Cập nhật sản phẩm Variant thành công",
                                    data=product_variant)
    @catch_exceptions
    def delete(self, request, sku, *args, **kwargs):
        product_variant = ProductVariantService.delete_product_variant(sku)
        if not product_variant:
            return res.response_error(message="Sản phẩm Variant không tồn tại!")
        return res.response_success(message="Xóa sản phẩm Variant thành công", data=product_variant)
