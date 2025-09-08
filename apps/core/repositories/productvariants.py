
from datetime import datetime

from apps.core.models.products import ProductVariant
from apps.utils import minio as S3
from apps.utils.decorator import *


class ProductVariantRepository:
    @staticmethod
    @catch_exceptions
    @log_sql
    def create(data: dict):
        product_variant = ProductVariant.objects.create(**data)
        return product_variant
    @staticmethod
    @catch_exceptions
    @log_sql
    def get_all():
        product_variant_list = list(ProductVariant.objects.all())
        return product_variant_list
    @staticmethod
    @catch_exceptions
    @log_sql
    def get_by_sku(sku : str):
        try:
            product_variant = ProductVariant.objects.get(sku=sku, is_deleted=False)
            return product_variant
        except ProductVariant.DoesNotExist:
            return None
    @staticmethod
    @catch_exceptions
    @log_sql
    def update(product_variant: ProductVariant, validated_data: dict):
        img_file = validated_data.pop("img", None)
        if img_file is not None:
            img_name = "img_product_" + datetime.now().strftime("%Y%m%d%H%M%S")
            img_url = S3.upload_image(img_file, img_name)
            product_variant.img = img_url
        for attr, value in validated_data.items():
            setattr(product_variant, attr, value)
        product_variant.save()
        return product_variant
    @staticmethod
    @catch_exceptions
    @log_sql
    def delete(product_variant: ProductVariant):
        product_variant.is_deleted = True
        product_variant.save()
        return product_variant
