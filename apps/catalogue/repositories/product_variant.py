

from apps.catalogue.models.products import ProductVariant
from apps.logging import logging_log as lg

class ProductVariantRepository:
    def get_product_variant_by_id(self, product_variant_id):
        return ProductVariant.objects.filter(id=product_variant_id).first()
        
product_variant_repository = ProductVariantRepository()