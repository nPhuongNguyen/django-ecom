from django.db import transaction
from apps.catalogue.repositories.product import product_repository
from apps.catalogue.repositories.attribute import attribute_repository
from apps.catalogue.repositories.product_attribute import product_attribute_repository
from rest_framework.exceptions import ValidationError
class ProducService:
    def create_product(self, product_data, attribute_ids):
        with transaction.atomic():
            product = product_repository.create_product(product_data)
            if len(attribute_ids) > 0:
                for attr_id in attribute_ids:
                    attribute = attribute_repository.get_attribute_by_id(attr_id=attr_id)
                    if not attribute:
                        raise ValidationError({
                        "attributes": f"Thuộc tính với ID {attr_id} không tồn tại trên hệ thống."
                    })
                    product_attribute_repository.create_product_attribute(product, attribute)
        return product
        
        
    
product_service = ProducService()