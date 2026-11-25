

from apps.catalogue.models.products import ProductVariant
from apps.logging import logging_log as lg

class ProductVariantRepository:
    def get_by_id(self, product_variant_id):
        return ProductVariant.objects.filter(id=product_variant_id).first()
    
    def create(self, product_variant_data):
        return ProductVariant.objects.create(**product_variant_data)

product_variant_repository = ProductVariantRepository()