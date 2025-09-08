from apps.core.repositories.productvariants import ProductVariantRepository
from apps.core.schema.productvariants import ProductVariantOutputSerializer
from apps.utils.decorator import *


class ProductVariantService:
    @staticmethod
    @catch_exceptions
    def create_product_variant(data):
        product_variant = ProductVariantRepository.create(data)
        product_variant_validate_serializer = ProductVariantOutputSerializer(product_variant)
        return product_variant_validate_serializer.data
    @staticmethod
    @catch_exceptions
    def get_product_variant_by_sku(sku: str):
        product_variant =  ProductVariantRepository.get_by_sku(sku)
        if product_variant is None:
            return None
        product_variant_validate_serializer = ProductVariantOutputSerializer(product_variant)
        return product_variant_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def get_all_products_variant():
        product_variant = ProductVariantRepository.get_all()
        product_variant_validate_serializer = ProductVariantOutputSerializer(product_variant,
                                                                              many = True)
        return product_variant_validate_serializer.data
    @staticmethod
    @catch_exceptions
    def update_product_variant(sku, validated_data):
        product_variant = ProductVariantRepository.get_by_sku(sku)
        if not product_variant:
            return None
        update_product_variant = ProductVariantRepository.update(product_variant, validated_data)
        product_variant_validate_serializer = ProductVariantOutputSerializer(update_product_variant)
        return product_variant_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def delete_product_variant(sku: str):
        product_variant = ProductVariantRepository.get_by_sku(sku)
        if not product_variant:
            return None
        delete_product_variant = ProductVariantRepository.delete(product_variant)
        product_variant_validate_serializer = ProductVariantOutputSerializer(delete_product_variant)
        return product_variant_validate_serializer.data
