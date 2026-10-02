from django.db import transaction
from apps.catalogue.repositories.product import product_repository
from apps.catalogue.repositories.attribute import attribute_repository
from apps.catalogue.repositories.product_attribute import product_attribute_repository
from rest_framework.exceptions import ValidationError
class ProductService:
    def create(self, product_data, attribute_ids):
        attribute_ids = attribute_ids or []
        list_attributes = []
        if attribute_ids:
            if len(attribute_ids) != len(set(attribute_ids)):
                raise ValidationError({
                    "attributes": "Danh sách thuộc tính không được trùng lặp."
                })
            list_attributes = attribute_repository.get_by_ids(attribute_ids)
            if len(list_attributes) != len(attribute_ids):
                existing_ids = {attr.id for attr in list_attributes}
                missing_ids = set(attribute_ids) - existing_ids
                raise ValidationError({
                    "attributes": f"Thuộc tính với ID {', '.join(map(str, missing_ids))} không tồn tại trên hệ thống."
                })
        with transaction.atomic():
            created_product = product_repository.create(product_data)
            for attr in list_attributes:
                product_attribute_repository.create(created_product, attr)
            return created_product
product_service = ProductService()